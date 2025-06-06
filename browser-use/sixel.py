# fork from: https://raw.githubusercontent.com/lubosz/python-sixel/refs/heads/main/sixel/converter.py

# -*- coding: utf-8 -*-
# Copyright 2012-2014 Hayaki Saito <user@zuse.jp>
# Copyright 2023 Lubosz Sarnecki <lubosz@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from io import StringIO, BytesIO
import sys

from PIL import Image


class SixelConverter:

    def __init__(self, file,
                 f8bit=False,
                 w=None,
                 h=None,
                 ncolor=256,
                 alpha_threshold=0,
                 chromakey=False,
                 fast=True):

        self.__alpha_threshold = alpha_threshold
        self.__chromakey = chromakey
        self._slots = [0] * 257
        self._fast = fast

        if ncolor >= 256:
            ncolor = 256

        self._ncolor = ncolor

        if f8bit:  # 8bit mode
            self.DCS = '\x90'
            self.ST = '\x9c'
        else:
            self.DCS = '\x1bP'
            self.ST = '\x1b\\'

        if isinstance(file, str):
            image = Image.open(file)
        elif isinstance(file, bytes):
            image = Image.open(BytesIO(file))
        elif isinstance(file, Image.Image):
            image = file
        else:
            raise TypeError(f"Invalid type {type(file)}, must be a file_path or PIL.Image.Image")
        image = image.convert("RGB").convert("P",
                                             palette=Image.Palette.ADAPTIVE,
                                             colors=ncolor)
        if w or h:
            width, height = image.size
            if not w:
                w = width
            if not h:
                h = height
            image = image.resize((w, h))

        self.palette = image.getpalette()
        self.data = image.getdata()
        self.width, self.height = image.size

        if alpha_threshold > 0:
            self.rawdata = Image.open(file).convert("RGBA").getdata()

    def __write_header(self, output):
        # start Device Control String (DCS)
        output.write(self.DCS)

        # write header
        aspect_ratio = 7  # means 1:1
        if self.__chromakey:
            background_option = 2
        else:
            background_option = 1
        dpi = 75  # dummy value
        template = '%d;%d;%dq"1;1;%d;%d'
        args = (aspect_ratio, background_option, dpi, self.width, self.height)
        output.write(template % args)

    def __write_palette_section(self, output):

        palette = self.palette

        # write palette section
        for i in range(0, self._ncolor * 3, 3):
            no = i / 3
            r = palette[i + 0] * 100 / 256
            g = palette[i + 1] * 100 / 256
            b = palette[i + 2] * 100 / 256
            output.write('#%d;2;%d;%d;%d' % (no, r, g, b))

    def __write_body_without_alpha_threshold(self, output, data):
        for n in range(0, self._ncolor):
            palette = self.palette
            r = palette[n * 3 + 0] * 100 / 256
            g = palette[n * 3 + 1] * 100 / 256
            b = palette[n * 3 + 2] * 100 / 256
            output.write('#%d;2;%d;%d;%d\n' % (n, r, g, b))
        height = self.height
        width = self.width
        for y in range(0, height, 6):
            if height - y <= 5:
                band = height - y
            else:
                band = 6
            buf = []
            set_ = set()

            def add_node(n_, s):
                nodes = []
                cache = 0
                count_ = 0
                if s:
                    nodes.append((0, s))
                for x in range(s, width):
                    count_ += 1
                    p = y * width + x
                    six_ = 0
                    for i in range(0, band):
                        d = data[p + width * i]
                        if d == n_:
                            six_ |= 1 << i
                        elif d not in set_:
                            set_.add(d)
                            add_node(d, x)
                    if six_ != cache:
                        nodes.append([cache, count_])
                        count_ = 0
                        cache = six_
                if cache != 0:
                    nodes.append([cache, count_])
                buf.append((n_, nodes))

            add_node(data[y * width], 0)

            for n, node in buf:
                output.write("#%d\n" % n)
                for six, count in node:
                    if count < 4:
                        output.write(chr(0x3f + six) * count)
                    else:
                        output.write('!%d%c' % (count, 0x3f + six))
                output.write("$\n")
            output.write("-\n")

    def __write_body_without_alpha_threshold_fast(self, output, data, key_color):
        height = self.height
        width = self.width
        n = 1
        for y in range(0, height):
            p = y * width
            cached_no = data[p]
            count = 1
            c = -1
            for x in range(0, width):
                color_no = data[p + x]
                if color_no == cached_no:  # and count < 255:
                    count += 1
                else:
                    if cached_no == key_color:
                        c = 0x3f
                    else:
                        c = 0x3f + n
                        if self._slots[cached_no] == 0:
                            palette = self.palette
                            r = palette[cached_no * 3 + 0] * 100 / 256
                            g = palette[cached_no * 3 + 1] * 100 / 256
                            b = palette[cached_no * 3 + 2] * 100 / 256
                            self._slots[cached_no] = 1
                            output.write('#%d;2;%d;%d;%d' % (cached_no, r, g, b))
                        output.write('#%d' % cached_no)
                    if count < 3:
                        output.write(chr(c) * count)
                    else:
                        output.write('!%d%c' % (count, c))
                    count = 1
                    cached_no = color_no
            if c != -1 and count > 1:
                if cached_no == key_color:
                    c = 0x3f
                else:
                    if self._slots[cached_no] == 0:
                        palette = self.palette
                        r = palette[cached_no * 3 + 0] * 100 / 256
                        g = palette[cached_no * 3 + 1] * 100 / 256
                        b = palette[cached_no * 3 + 2] * 100 / 256
                        self._slots[cached_no] = 1
                        output.write('#%d;2;%d;%d;%d' % (cached_no, r, g, b))
                    output.write('#%d' % cached_no)
                if count < 3:
                    output.write(chr(c) * count)
                else:
                    output.write('!%d%c' % (count, c))
            if n == 32:
                n = 1
                output.write('-')  # write sixel line separator
            else:
                n <<= 1
                output.write('$')  # write line terminator

    def __write_body_with_alpha_threshold(self, output, data, key_color):
        rawdata = self.rawdata
        height = self.height
        width = self.width
        max_run_length = 255
        n = 1
        for y in range(0, height):
            p = y * width
            cached_no = data[p]
            cached_alpha = rawdata[p][3]
            count = 1
            c = -1
            for x in range(0, width):
                color_no = data[p + x]
                alpha = rawdata[p + x][3]
                if color_no == cached_no:
                    if alpha == cached_alpha:
                        if count < max_run_length:
                            count += 1
                            continue
                if cached_no == key_color:
                    c = 0x3f
                elif cached_alpha < self.__alpha_threshold:
                    c = 0x3f
                else:
                    c = n + 0x3f
                if count == 1:
                    output.write('#%d%c' % (cached_no, c))
                elif count == 2:
                    output.write('#%d%c%c' % (cached_no, c, c))
                    count = 1
                else:
                    output.write('#%d!%d%c' % (cached_no, count, c))
                    count = 1
                cached_no = color_no
                cached_alpha = alpha
            if c != -1:
                if cached_no == key_color:
                    c = 0x3f
                if count == 1:
                    output.write('#%d%c' % (cached_no, c))
                elif count == 2:
                    output.write('#%d%c%c' % (cached_no, c, c))
                else:
                    output.write('#%d!%d%c' % (cached_no, count, c))
            output.write('$')  # write line terminator
            if n == 32:
                n = 1
                output.write('-')  # write sixel line separator
            else:
                n <<= 1

    def __write_body_section(self, output):
        data = self.data
        if self.__chromakey:
            key_color = data[0]
        else:
            key_color = -1
        if self.__alpha_threshold == 0:
            if self._fast:
                self.__write_body_without_alpha_threshold_fast(output, data, key_color)
            else:
                self.__write_body_without_alpha_threshold(output, data)
        else:
            self.__write_body_with_alpha_threshold(output, data, key_color)

    def __write_terminator(self, output):
        # write ST
        output.write(self.ST)  # terminate Device Control String

    def getvalue(self):
        output = StringIO()

        try:
            self.write(output)
            value = output.getvalue()

        finally:
            output.close()

        return value

    def write(self, output, body_only=False):
        if not body_only:
            self.__write_header(output)
        self.__write_body_section(output)
        if not body_only:
            self.__write_terminator(output)


def display(pil_image):
    c = SixelConverter(pil_image)
    c.write(sys.stdout)
    sys.stdout.write('\n')
    sys.stdout.flush()

