#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Flaress Demodulation Test
# GNU Radio version: 3.7.13.5
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from ecss import variables_loop_filter
from gnuradio import blocks
from gnuradio import channels
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import ecss
import flaress
import math
import pmt
import sip
import sys
from gnuradio import qtgui


class flaress_demodulation_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Flaress Demodulation Test")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Flaress Demodulation Test")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "flaress_demodulation_test")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 320000
        self.ss = ss = False
        self.sps = sps = 32
        self.reset = reset = False
        self.order = order = 2
        self.noise = noise = 0.0
        self.n_bit = n_bit = 38
        self.freq_offset = freq_offset = 0.0
        self.coeff = coeff = variables_loop_filter.coefficients(100, 0.707, 0, 5, 10, 0.707, samp_rate)

        ##################################################
        # Blocks
        ##################################################
        self._ss_options = (False, True, )
        self._ss_labels = ('False', 'True', )
        self._ss_group_box = Qt.QGroupBox('Signal Search Enable')
        self._ss_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ss_button_group = variable_chooser_button_group()
        self._ss_group_box.setLayout(self._ss_box)
        for i, label in enumerate(self._ss_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ss_box.addWidget(radio_button)
        	self._ss_button_group.addButton(radio_button, i)
        self._ss_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ss_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ss_options.index(i)))
        self._ss_callback(self.ss)
        self._ss_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ss(self._ss_options[i]))
        self.top_grid_layout.addWidget(self._ss_group_box, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._order_options = (2, 3, )
        self._order_labels = (str(self._order_options[0]), str(self._order_options[1]), )
        self._order_group_box = Qt.QGroupBox('PLL order')
        self._order_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._order_button_group = variable_chooser_button_group()
        self._order_group_box.setLayout(self._order_box)
        for i, label in enumerate(self._order_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._order_box.addWidget(radio_button)
        	self._order_button_group.addButton(radio_button, i)
        self._order_callback = lambda i: Qt.QMetaObject.invokeMethod(self._order_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._order_options.index(i)))
        self._order_callback(self.order)
        self._order_button_group.buttonClicked[int].connect(
        	lambda i: self.set_order(self._order_options[i]))
        self.top_grid_layout.addWidget(self._order_group_box, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._noise_range = Range(0.0, 10.0, 0.05, 0.0, 50)
        self._noise_win = RangeWidget(self._noise_range, self.set_noise, 'Noise Channel', "counter_slider", float)
        self.top_grid_layout.addWidget(self._noise_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._n_bit_range = Range(4, 52, 1, 38, 50)
        self._n_bit_win = RangeWidget(self._n_bit_range, self.set_n_bit, 'PLL N bits', "counter_slider", int)
        self.top_grid_layout.addWidget(self._n_bit_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_offset_range = Range(0.0, 10000.0, 100, 0.0, 50)
        self._freq_offset_win = RangeWidget(self._freq_offset_range, self.set_freq_offset, 'Frequency offset Channel', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freq_offset_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._reset_options = (False, True, )
        self._reset_labels = ('False', 'True', )
        self._reset_group_box = Qt.QGroupBox('Coherency Reset')
        self._reset_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._reset_button_group = variable_chooser_button_group()
        self._reset_group_box.setLayout(self._reset_box)
        for i, label in enumerate(self._reset_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._reset_box.addWidget(radio_button)
        	self._reset_button_group.addButton(radio_button, i)
        self._reset_callback = lambda i: Qt.QMetaObject.invokeMethod(self._reset_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._reset_options.index(i)))
        self._reset_callback(self.reset)
        self._reset_button_group.buttonClicked[int].connect(
        	lambda i: self.set_reset(self._reset_options[i]))
        self.top_grid_layout.addWidget(self._reset_group_box, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0 = qtgui.time_sink_f(
        	1024, #size
        	samp_rate, #samp_rate
        	'Demodulator Output', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0_0_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_0_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_0_win, 8, 0, 2, 3)
        for r in range(8, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	samp_rate, #samp_rate
        	'PLL Phase Error Output', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', 'Time')

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['Frequency', 'Phase Error', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 4, 0, 1, 3)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title('PLL Frequency Output')

        labels = ['Freq', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(True)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win, 5, 0, 1, 3)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	'Input Signal Spectrum', #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)

        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 2, 0, 2, 3)
        for r in range(2, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.flaress_null_sink_0 = flaress.null_sink(flaress.sizeof_long*1)
        self.ecss_signal_search_fft_hier_0 = ecss.signal_search_fft_hier(ss, 1024*16, 1, False, firdes.WIN_BLACKMAN_hARRIS, 10000, 5000, 100.0, 10.0, samp_rate)
        self.ecss_pll_0 = ecss.pll(samp_rate, order, n_bit, (coeff), 10000, 5000)
        self.ecss_demodulator_0 = ecss.demodulator(8, 6.28/100, 2, 16000, sps, 0.045, 1.0, 1.0, 1.5, 1, digital.IR_MMSE_8TAP, digital.TED_MUELLER_AND_MULLER, digital.constellation_bpsk().base(), 128, ([]), 1, 0, samp_rate)
        self.ecss_agc_0 = ecss.agc(10.0, 1.0, 1.0, 65536.0, samp_rate)
        self.channels_channel_model_0_0 = channels.channel_model(
        	noise_voltage=noise,
        	frequency_offset=freq_offset,
        	epsilon=1.0,
        	taps=(1.0 + 1.0j, ),
        	noise_seed=0,
        	block_tags=False
        )
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_gr_complex*1, '', ""); self.blocks_tag_debug_0.set_display(True)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/mnt/c/Users/amir/WSL/grc/FlowGraps/FlaReSS/files/sw150kHz_swr10kHz-s_tc4kbps_mi1.0.dat', True)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/mnt/c/Users/amir/WSL/grc/FlowGraps/FlaReSS/files/Demodulated_data.bin', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_0_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.channels_channel_model_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.channels_channel_model_0_0, 0), (self.ecss_agc_0, 0))
        self.connect((self.ecss_agc_0, 0), (self.ecss_signal_search_fft_hier_0, 0))
        self.connect((self.ecss_demodulator_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.ecss_demodulator_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.ecss_pll_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.ecss_pll_0, 2), (self.ecss_demodulator_0, 0))
        self.connect((self.ecss_pll_0, 3), (self.flaress_null_sink_0, 0))
        self.connect((self.ecss_pll_0, 1), (self.qtgui_number_sink_0, 0))
        self.connect((self.ecss_pll_0, 2), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.ecss_signal_search_fft_hier_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.ecss_signal_search_fft_hier_0, 0), (self.ecss_pll_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "flaress_demodulation_test")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_ss(self):
        return self.ss

    def set_ss(self, ss):
        self.ss = ss
        self._ss_callback(self.ss)
        self.ecss_signal_search_fft_hier_0.set_enable(self.ss)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_reset(self):
        return self.reset

    def set_reset(self, reset):
        self.reset = reset
        self._reset_callback(self.reset)

    def get_order(self):
        return self.order

    def set_order(self, order):
        self.order = order
        self._order_callback(self.order)
        self.ecss_pll_0.set_order(self.order)

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise
        self.channels_channel_model_0_0.set_noise_voltage(self.noise)

    def get_n_bit(self):
        return self.n_bit

    def set_n_bit(self, n_bit):
        self.n_bit = n_bit

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.channels_channel_model_0_0.set_frequency_offset(self.freq_offset)

    def get_coeff(self):
        return self.coeff

    def set_coeff(self, coeff):
        self.coeff = coeff
        self.ecss_pll_0.set_coefficients((self.coeff))


def main(top_block_cls=flaress_demodulation_test, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
