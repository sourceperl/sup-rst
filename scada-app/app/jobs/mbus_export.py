"""Export some tags to external modbus server."""


import datetime
import time

import schedule
from pyModbusTCP.client import ModbusClient
from sqlalchemy import Engine

from ..db.sup_rst import ScadaData

# some consts
PROCESS_NAME = 'mbus-export'


# define tasks
class JobMbusExport:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        # init schedule
        schedule.every(1).minute.do(self._task_export_avion)

    def _task_export_avion(self):
        """Build a list of TS/TM tags and export it to "T-Box MS Avion côté zone" device."""
        # DB sup_rst
        scada = ScadaData(engine=self.engine, process=PROCESS_NAME)
        # ts
        ts_l1_mel_m = scada.ts('ARLM_L1_M', False)
        ts_l2_mel_m = scada.ts('ARLM_L2_M', False)
        ts_mel_m = ts_l1_mel_m or ts_l2_mel_m                  # @20486
        # tm
        l_tm = list()
        l_tm.append(0)                                         # @20536
        l_tm.append(0)                                         # @20537
        l_tm.append(0)                                         # @20538
        l_tm.append(0)                                         # @20539
        l_tm.append(scada.tm('ARL_AE1_PCS', 0))                  # @20540
        l_tm.append(scada.tm('ARL_AE1_WBE', 0))                  # @20541
        l_tm.append(scada.tm('ARL_AE1_CO2', 0))                  # @20542
        l_tm.append(scada.tm('Q_ARL_AE1', 0))                    # @20543
        l_tm.append(scada.tm('ARL_AE1_ANC', 0))                  # @20544
        l_tm.append(scada.tm('AVION_PCS', 0))                    # @20545
        l_tm.append(scada.tm('AVION_WBE', 0))                    # @20546
        l_tm.append(scada.tm('AVION_HP_CO2', 0))                 # @20547
        l_tm.append(scada.tm('AVION_ANC', 0))                    # @20548
        l_tm.append(scada.tm('Q_ARL_AO', 0))                     # @20549
        l_tm.append(scada.tm('ARL_AO2_PCS', 0))                  # @20550
        l_tm.append(scada.tm('ARL_AO2_WBE', 0))                  # @20551
        l_tm.append(scada.tm('ARL_AO2_CO2', 0))                  # @20552
        l_tm.append(scada.tm('ARL_AO2_ANC', 0))                  # @20553
        # add life indicator (srv minute)
        l_tm.append(datetime.datetime.now().minute)            # @20554
        # Q Arleux mel.
        l_tm.append(scada.tm('ARLM_Q', 0))                       # @20555
        l_tm.append(0)                                         # @20556
        l_tm.append(0)                                         # @20557
        l_tm.append(0)                                         # @20558
        l_tm.append(0)                                         # @20559
        # network pressure at Arleux injection point (17PIT18B)
        l_tm.append(int(round(scada.tm('ARLM_P_AO1', 0)/10.0)))  # @20560
        # normalize modbus data
        ts_mel_m = bool(ts_mel_m)
        l_tm = [max(min(int(round(x)), 0xffff), 0x000) for x in l_tm]
        # do modbus write
        c = ModbusClient(host='163.111.181.18', unit_id=1, auto_open=True)
        c.write_single_coil(20486, ts_mel_m)
        c.write_multiple_registers(20536, l_tm)
        c.close()

    def run(self):
        # first call at startup
        self._task_export_avion()

        # main loop
        while True:
            schedule.run_pending()
            time.sleep(1.0)
