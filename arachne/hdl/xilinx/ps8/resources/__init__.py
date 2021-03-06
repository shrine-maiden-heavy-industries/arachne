# SPDX-License-Identifier: BSD-3-Clause
from .common import PS8Resource, MIOSet

from .can    import CANResource
from .csu    import CSUResource
from .ddr    import DDRResource, DDRType, DDRModuleType
from .dma    import DMAResource
from .dp     import DPResource
from .eth    import ETHResource
from .gpio   import GPIOResource
from .i2c    import I2CResource
from .nand   import NANDResource
from .pcie   import PCIEResource, PCIEPortType, PCIEPortType
from .pjtag  import PJTAGResource
from .pmu    import PMUResource
from .qspi   import QSPIResource, QSPIMode, QSPIDataMode
from .sata   import SATAResource
from .sd     import SDResource
from .spi    import SPIResource
from .swdt   import SWDTResource
from .tcc    import TCCResource
from .trace  import TraceResource
from .uart   import UARTResource
from .usb    import USBResource

__all__ = (
	'PS8Resource', 'MIOSet',

	'CANResource',
	'CSUResource',
	'DDRResource', 'DDRType', 'DDRModuleType',
	'DMAResource',
	'DPResource',
	'ETHResource',
	'GPIOResource',
	'I2CResource',
	'NANDResource',
	'PCIEResource', 'PCIEPortType', 'PCIEPortType',
	'PJTAGResource',
	'PMUResource',
	'QSPIResource', 'QSPIMode', 'QSPIDataMode',
	'SATAResource',
	'SDResource',
	'SPIResource',
	'SWDTResource',
	'TCCResource',
	'TraceResource',
	'UARTResource',
	'USBResource',
)
