#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FLareSS combined test
# GNU Radio version: 3.8.0.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import channels
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import ecss
import flaress
import math
from gnuradio import qtgui

class flaress_combined_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FLareSS combined test")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FLareSS combined test")
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

        self.settings = Qt.QSettings("GNU Radio", "flaress_combined_test")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.ss = ss = False
        self.reset = reset = False
        self.order = order = 2
        self.n_bit = n_bit = 38
        self.cof = cof = 10.0
        self.coeff = coeff = ecss.variables_loop_filter.coefficients(100, 0.707, 0, 5, 10, 0.707, samp_rate)
        self.bit_rate = bit_rate = 16000

        ##################################################
        # Blocks
        ##################################################
        # Create the options list
        self._ss_options = (False, True, )
        # Create the labels list
        self._ss_labels = ('False', 'True', )
        # Create the combo box
        # Create the radio buttons
        self._ss_group_box = Qt.QGroupBox('Signal Search Enable' + ": ")
        self._ss_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ss_button_group = variable_chooser_button_group()
        self._ss_group_box.setLayout(self._ss_box)
        for i, _label in enumerate(self._ss_labels):
            radio_button = Qt.QRadioButton(_label)
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
        # Create the options list
        self._reset_options = (False, True, )
        # Create the labels list
        self._reset_labels = ('False', 'True', )
        # Create the combo box
        # Create the radio buttons
        self._reset_group_box = Qt.QGroupBox('Coherency Reset' + ": ")
        self._reset_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._reset_button_group = variable_chooser_button_group()
        self._reset_group_box.setLayout(self._reset_box)
        for i, _label in enumerate(self._reset_labels):
            radio_button = Qt.QRadioButton(_label)
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
        # Create the options list
        self._order_options = (2, 3, )
        # Create the labels list
        self._order_labels = ('', '', )
        # Create the combo box
        # Create the radio buttons
        self._order_group_box = Qt.QGroupBox('PLL order' + ": ")
        self._order_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._order_button_group = variable_chooser_button_group()
        self._order_group_box.setLayout(self._order_box)
        for i, _label in enumerate(self._order_labels):
            radio_button = Qt.QRadioButton(_label)
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
        self._n_bit_range = Range(4, 52, 1, 38, 50)
        self._n_bit_win = RangeWidget(self._n_bit_range, self.set_n_bit, 'PLL N bits', "counter_slider", int)
        self.top_grid_layout.addWidget(self._n_bit_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._cof_range = Range(10.0, 10000.0, 100.0, 10.0, 50)
        self._cof_win = RangeWidget(self._cof_range, self.set_cof, 'LPF cut-off frequency', "counter_slider", float)
        self.top_grid_layout.addWidget(self._cof_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            1024 , #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'Output Signal Spectrum', #name
            1
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(True)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_0_win, 7, 0, 2, 3)
        for r in range(7, 9):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.low_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                cof,
                10,
                firdes.WIN_HAMMING,
                6.76))
        self.flaress_selector_0 = flaress.selector(gr.sizeof_char*1, 0, 2, 1)
        self.ecss_signal_search_fft_hier_0 = ecss.signal_search_fft_hier(ss, 1024*16, 1, False, firdes.WIN_BLACKMAN_hARRIS, 10000, 5000, 100.0, 10.0, samp_rate)
        self.ecss_pll_0 = ecss.pll(samp_rate, order, n_bit, coeff, 10000, 5000)
        self.ecss_phase_converter_0 = ecss.phase_converter(n_bit)
        self.ecss_modulator_0 = ecss.modulator(7, 2, [79,-109], 0, False, samp_rate, bit_rate, 1, 0, 0, 0.35,  int(samp_rate/11), True, 16000)
        self.ecss_gain_phase_accumulator_0 = ecss.gain_phase_accumulator(reset, 221, 240)
        self.ecss_coherent_phase_modulator_0 = ecss.coherent_phase_modulator(n_bit, 1)
        self.ecss_agc_0 = ecss.agc(10.0, 1.0, 1.0, 65536.0, samp_rate)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=0,
            frequency_offset=0,
            epsilon=1.0,
            taps=[1.0 + 1.0j],
            noise_seed=0,
            block_tags=False)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate/8/2,True)
        self.blocks_null_sink_3 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_2 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_char*1, '/data/andrej/git/esa/Flowgraphs/files/Convolutionally_encoded_CADU.bin', True, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/data/andrej/git/esa/Flowgraphs/files/CADU.bin', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 12000, 1, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ecss_phase_converter_0, 'async_out'), (self.ecss_coherent_phase_modulator_0, 'async_in'))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.flaress_selector_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.flaress_selector_0, 1))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.ecss_modulator_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.ecss_agc_0, 0))
        self.connect((self.ecss_agc_0, 0), (self.ecss_signal_search_fft_hier_0, 0))
        self.connect((self.ecss_coherent_phase_modulator_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.ecss_gain_phase_accumulator_0, 0), (self.ecss_coherent_phase_modulator_0, 0))
        self.connect((self.ecss_modulator_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.ecss_phase_converter_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.ecss_pll_0, 0), (self.blocks_null_sink_1, 0))
        self.connect((self.ecss_pll_0, 2), (self.blocks_null_sink_2, 0))
        self.connect((self.ecss_pll_0, 1), (self.blocks_null_sink_3, 0))
        self.connect((self.ecss_pll_0, 3), (self.ecss_gain_phase_accumulator_0, 0))
        self.connect((self.ecss_signal_search_fft_hier_0, 0), (self.ecss_pll_0, 0))
        self.connect((self.flaress_selector_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.ecss_phase_converter_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "flaress_combined_test")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate/8/2)
        self.blocks_throttle_0_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cof, 10, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)

    def get_ss(self):
        return self.ss

    def set_ss(self, ss):
        self.ss = ss
        self._ss_callback(self.ss)
        self.ecss_signal_search_fft_hier_0.set_enable(self.ss)

    def get_reset(self):
        return self.reset

    def set_reset(self, reset):
        self.reset = reset
        self._reset_callback(self.reset)
        self.ecss_gain_phase_accumulator_0.set_reset(self.reset)

    def get_order(self):
        return self.order

    def set_order(self, order):
        self.order = order
        self._order_callback(self.order)
        self.ecss_pll_0.set_order(self.order)

    def get_n_bit(self):
        return self.n_bit

    def set_n_bit(self, n_bit):
        self.n_bit = n_bit

    def get_cof(self):
        return self.cof

    def set_cof(self, cof):
        self.cof = cof
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cof, 10, firdes.WIN_HAMMING, 6.76))

    def get_coeff(self):
        return self.coeff

    def set_coeff(self, coeff):
        self.coeff = coeff
        self.ecss_pll_0.set_coefficients(self.coeff)

    def get_bit_rate(self):
        return self.bit_rate

    def set_bit_rate(self, bit_rate):
        self.bit_rate = bit_rate



def main(top_block_cls=flaress_combined_test, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
