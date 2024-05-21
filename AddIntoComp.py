# -- coding: utf-8 --
import copy
import random
import cloudpss  # 导入CLoudPSS内部SDK模块
import os
import json
import zmq
import Component_pb2
from cloudpss.model.implements.component import Component  # 内部元件类模块使用

# tk = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjA0MSwidXNlcm5hbWUiOiJrcmlzMzYwIiwic2NvcGVzIjpbXSwidHlwZSI6ImFwcGx5IiwiZXhwIjoxNjkzMTIwMDIzLCJpYXQiOjE2NjIwMTYwMjN9.lUND4iX7UzAfw1HVUzwVo2cEJZUNEe7wUiZ2QpyrKCukk0LE5KiWDgPSoTVPsaN2lPCJqyuzPEMNPeKNLPm_FWFzTPxPsAvJ7GgDr0htkrIuAfJ08_tT71mSABujv3rcvq8GDfU4mT5qCRNT7IY4wnTKO5yRyENoifV9ME3nvpM';
# tk = 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsInNjb3BlcyI6W10sInR5cGUiOiJhcHBseSIsImV4cCI6MTY3MDk4MzIzMywiaWF0IjoxNjcwODk2ODMzfQ.AuN-tgGTTTPgpEt3uoXTNjUjyGt_seV-gl9kDgHMkmxYqbHsjH_8HsEsRhs6RYQcq7KATkCY1-EXJH3fGh4l1Q'
# cloudpss.setToken(
#     'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsInNjb3BlcyI6W10sInR5cGUiOiJhcHBseSIsImV4cCI6MTcwMTkyODY4MywiaWF0IjoxNjcwODI0NjgzfQ.gjqFyFd451nsR3F1UyUQouIp0yA-Yi2jY7_Gp1zFlKkJlrX5R2F8GlXxv0hlflGOkO59YZEvkqT0OnKdMBoCsQ')
# os.environ['CLOUDPSS_API_URL'] = 'http://192.168.3.142/'
cloudpss.setToken(
    'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjA0MSwidXNlcm5hbWUiOiJrcmlzMzYwIiwic2NvcGVzIjpbXSwidHlwZSI6ImFwcGx5IiwiZXhwIjoxNzAyMTA1NjU0LCJpYXQiOjE2NzEwMDE2NTR9.RSIw6hVP45C2lbPuARu7Zirqvq3J3fmqv-eJ2Fpu-wSEditZwwWnkovN3-zOmFhZ1hqLdZs9H6SUaHLEcR55GlaCmtXC2mzG4vqjfDWDxfGnT2GrJznUr8ZTR9kXqW6cSc3MntdAifmOIAxHKRc0zHiEc1k64zAW12lercz8kFw')
os.environ['CLOUDPSS_API_URL'] = 'https://cloudpss.net'
# cloudpss.setToken('eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsInNjb3BlcyI6W10sInR5cGUiOiJhcHBseSIsImV4cCI6MTY3MzQ4OTEzNSwiaWF0IjoxNjcwODk3MTM1fQ.Gu-pmHOg4zWrnV2C0anb9UbFwf7A-D5wLJBNYYibmU8S2eVTxnlbO9O7iJ8SHDgWtv_o72utQedSys0UBMnKWw')
# 项目构建与读取
with open('source.json', 'r', encoding='utf-8') as f:
    compLib = json.load(f)
print('compLib.keys :')
print(compLib.keys())
project = cloudpss.Model.fetch('model/kris360/modelTest')


# 创建断路器元件函数
def AddBreaker(ID, Name, Description, NormalOpen, RatedCurrent, BreakingCapacity, PSRType, EquipmentContainer,
               BaseVoltage, Terminal_1, Terminal_2, Location):
    # 通过生成的Json文件构建断路器模板
    BreakerJson = compLib['Breaker'];
    CBreakerJson = copy.deepcopy(BreakerJson)  # 防止内存空间覆盖
    Breaker = Component(CBreakerJson)
    # 参数导入
    Breaker.args['ID'] = ID
    Breaker.args['Name'] = Name
    Breaker.args['BaseVoltage'] = BaseVoltage
    Breaker.args['BreakingCapacity'] = BreakingCapacity
    Breaker.args['Description'] = Description;
    Breaker.args['EquipmentContainer'] = EquipmentContainer
    Breaker.args['Location'] = Location
    Breaker.args['NormalOpen'] = NormalOpen
    Breaker.args['PSRType'] = PSRType
    Breaker.args['RatedCurrent'] = RatedCurrent
    Breaker.pins['Terminal_1'] = Terminal_1
    Breaker.pins['Terminal_2'] = Terminal_2
    print(ID, Name, Description, NormalOpen, RatedCurrent, BreakingCapacity, PSRType, EquipmentContainer, BaseVoltage,
          Terminal_1, Terminal_2, Location)
    Breaker.position['x'] = random.randint(100, 500)
    Breaker.position['y'] = random.randint(100, 500)
    # CloudPSS平台读取元件的唯一ID
    Breaker.id = ID
    project.revision.implements.diagram.cells[ID] = Breaker
    print('断路器元件生成成功')
    # 将生成的元件更新至算例中
    # project.update(project);


# 创建负荷开关元件函数
def AddLoadBreakSwitch(ID, Name, NormalOpen, RatedCurrent, BreakingCapacity, PSRType, EquipmentContainer, BaseVoltage,
                       Terminal_1, Terminal_2, Location):
    LoadBreakSwitchJson = compLib['LoadBreakSwitch'];
    CLoadBreakSwitchJson = copy.deepcopy(LoadBreakSwitchJson)
    LoadBreakSwitch = Component(CLoadBreakSwitchJson)
    LoadBreakSwitch.args['ID'] = ID
    LoadBreakSwitch.args['Name'] = Name
    LoadBreakSwitch.args['BaseVoltage'] = BaseVoltage
    LoadBreakSwitch.args['BreakingCapacity'] = BreakingCapacity
    LoadBreakSwitch.args['EquipmentContainer'] = EquipmentContainer
    LoadBreakSwitch.args['Location'] = Location
    LoadBreakSwitch.args['NormalOpen'] = NormalOpen
    LoadBreakSwitch.args['PSRType'] = PSRType
    LoadBreakSwitch.args['RatedCurrent'] = RatedCurrent
    LoadBreakSwitch.pins['Terminal_1'] = Terminal_1
    LoadBreakSwitch.pins['Terminal_2'] = Terminal_2
    print(ID, Name, NormalOpen, RatedCurrent, BreakingCapacity, PSRType, EquipmentContainer, BaseVoltage, Terminal_1,
          Terminal_2, Location)
    LoadBreakSwitch.position['x'] = random.randint(100, 500)
    LoadBreakSwitch.position['y'] = random.randint(100, 500)
    LoadBreakSwitch.id = ID
    project.revision.implements.diagram.cells[ID] = LoadBreakSwitch
    print('负荷开关元件生成成功')
    # project.update(project)


# 创建隔离开关元件函数
def AddDisconnector(ID, Name, NormalOpen, RatedCurrent, PSRType, EquipmentContainer, BaseVoltage, Terminal_1,
                    Terminal_2, Location):
    DisconnectorJson = compLib['Disconnector'];
    CDisconnectorJson = copy.deepcopy(DisconnectorJson)
    Disconnector = Component(CDisconnectorJson)
    Disconnector.args['ID'] = ID
    Disconnector.args['Name'] = Name
    Disconnector.args['BaseVoltage'] = BaseVoltage
    Disconnector.args['EquipmentContainer'] = EquipmentContainer
    Disconnector.args['Location'] = Location
    Disconnector.args['NormalOpen'] = NormalOpen
    Disconnector.args['PSRType'] = PSRType
    Disconnector.args['RatedCurrent'] = RatedCurrent
    Disconnector.pins['Terminal_1'] = Terminal_1
    Disconnector.pins['Terminal_2'] = Terminal_2
    print(ID, Name, NormalOpen, RatedCurrent, PSRType, EquipmentContainer, BaseVoltage, Terminal_1, Terminal_2,
          Location)
    Disconnector.position['x'] = random.randint(100, 500)
    Disconnector.position['y'] = random.randint(100, 500)
    Disconnector.id = ID
    project.revision.implements.diagram.cells[ID] = Disconnector
    print('隔离开关元件生成成功')
    # project.update(project);


# 创建交流导线段元件函数
def AddACLineSegment(ID, Name, Length, R, X, B, G, PSRType, EquipmentContainer, BaseVoltage, Terminal_1, Terminal_2,
                     Location):
    ACLineSegmentJson = compLib['ACLineSegment'];
    CACLineSegmentJson = copy.deepcopy(ACLineSegmentJson)
    ACLineSegment = Component(CACLineSegmentJson)
    ACLineSegment.args['ID'] = ID
    ACLineSegment.args['Name'] = Name
    ACLineSegment.args['G'] = G
    ACLineSegment.args['B'] = B
    ACLineSegment.args['BaseVoltage'] = BaseVoltage
    ACLineSegment.args['Length'] = Length
    ACLineSegment.args['X'] = X
    ACLineSegment.args['R'] = R
    ACLineSegment.args['PSRType'] = PSRType
    ACLineSegment.args['EquipmentContainer'] = EquipmentContainer
    ACLineSegment.args['Location'] = Location
    ACLineSegment.pins['Terminal_1'] = Terminal_1
    ACLineSegment.pins['Terminal_2'] = Terminal_2
    print(ID, Name, Length, R, X, B, G, PSRType, EquipmentContainer, BaseVoltage, Terminal_1, Terminal_2, Location)
    ACLineSegment.position['x'] = random.randint(100, 500)
    ACLineSegment.position['y'] = random.randint(100, 500)
    ACLineSegment.id = ID
    project.revision.implements.diagram.cells[ID] = ACLineSegment
    print('交流导线段元件生成成功')
    # project.update(project);


# 创建等效负荷元件函数
def AddEnergyConsumer(ID, Name, CustomerCount, P, Q, PFixed, QFixed, Grounded, Terminal_1):
    EnergyConsumerJson = compLib['EnergyConsumer'];
    CEnergyConsumerJson = copy.deepcopy(EnergyConsumerJson)
    EnergyConsumer = Component(CEnergyConsumerJson)
    EnergyConsumer.args['ID'] = ID
    EnergyConsumer.args['Name'] = Name
    EnergyConsumer.args['CustomerCount'] = CustomerCount
    EnergyConsumer.args['P'] = P
    EnergyConsumer.args['Q'] = Q
    EnergyConsumer.args['PFixed'] = PFixed
    EnergyConsumer.args['QFixed'] = QFixed
    EnergyConsumer.args['Grounded'] = Grounded
    EnergyConsumer.pins['Terminal_1'] = Terminal_1
    print(ID, Name, CustomerCount, P, Q, PFixed, QFixed, Grounded, Terminal_1)
    EnergyConsumer.position['x'] = random.randint(100, 500)
    EnergyConsumer.position['y'] = random.randint(100, 500)
    EnergyConsumer.id = ID
    project.revision.implements.diagram.cells[ID] = EnergyConsumer
    print('等效负荷元件生成成功')
    # project.update(project);


# 创建光伏发电单元元件函数
def AddPhotoVoltaicUnit(ID, Name, MaxP, MinP, PowerElectronicsConnection, Location, Terminal_1):
    PhotoVoltaicUnitJson = compLib['PhotoVoltaicUnit'];
    CPhotoVoltaicUnitJson = copy.deepcopy(PhotoVoltaicUnitJson)
    PhotoVoltaicUnit = Component(CPhotoVoltaicUnitJson)
    PhotoVoltaicUnit.args['ID'] = ID
    PhotoVoltaicUnit.args['Name'] = Name
    PhotoVoltaicUnit.args['MaxP'] = MaxP
    PhotoVoltaicUnit.args['MinP'] = MinP
    PhotoVoltaicUnit.args['PowerElectronicsConnection'] = PowerElectronicsConnection
    PhotoVoltaicUnit.args['Location'] = Location
    PhotoVoltaicUnit.pins['Terminal_1'] = Terminal_1
    print(ID, Name, MaxP, MinP, PowerElectronicsConnection, Location, Terminal_1)
    PhotoVoltaicUnit.position['x'] = random.randint(100, 500)
    PhotoVoltaicUnit.position['y'] = random.randint(100, 500)
    PhotoVoltaicUnit.id = ID
    project.revision.implements.diagram.cells[ID] = PhotoVoltaicUnit
    print('光伏发电单元元件生成成功')
    # project.update(project);


# 创建储能元件函数
def AddBatteryUnit(ID, Name, MaxP, MinP, RatedE, StoredE, PowerElectronicsConnection, Location, Terminal_1):
    BatteryUnitJson = compLib['BatteryUnit'];
    CBatteryUnitJson = copy.deepcopy(BatteryUnitJson)
    BatteryUnit = Component(CBatteryUnitJson)
    BatteryUnit.args['ID'] = ID
    BatteryUnit.args['Name'] = Name
    BatteryUnit.args['MaxP'] = MaxP
    BatteryUnit.args['MinP'] = MinP
    BatteryUnit.args['RatedE'] = RatedE
    BatteryUnit.args['StoredE'] = StoredE
    BatteryUnit.args['PowerElectronicsConnection'] = PowerElectronicsConnection
    BatteryUnit.args['Location'] = Location
    BatteryUnit.pins['Terminal_1'] = Terminal_1
    print(ID, Name, MaxP, MinP, RatedE, StoredE, PowerElectronicsConnection, Location, Terminal_1)
    BatteryUnit.position['x'] = random.randint(100, 500)
    BatteryUnit.position['y'] = random.randint(100, 500)
    BatteryUnit.id = ID
    project.revision.implements.diagram.cells[ID] = BatteryUnit
    print('储能元件生成成功')
    # project.update(project);


# 创建端子元件函数
def AddTerminal(SequenceNumber, Phases, ConnectivityNode, ConductingEquipment, Terminal_1):
    TerminalJson = compLib['Terminal'];
    CTerminalJson = copy.deepcopy(TerminalJson)
    Terminal = Component(CTerminalJson)
    Terminal.args['SequenceNumber'] = SequenceNumber
    Terminal.args['Phases'] = Phases
    Terminal.args['ConnectivityNode'] = ConnectivityNode
    Terminal.args['ConductingEquipment'] = ConductingEquipment
    Terminal.pins['Terminal_1'] = Terminal_1
    print(SequenceNumber, Phases, ConnectivityNode, ConductingEquipment, Terminal_1)
    Terminal.position['x'] = random.randint(100, 500)
    Terminal.position['y'] = random.randint(100, 500)
    Terminal.id = Terminal_1
    project.revision.implements.diagram.cells[Terminal_1] = Terminal
    print('端子元件生成成功')
    # project.update(project);


# 创建单相交流电压源
def AddnewACVoltageSource_1p(Name, Grnd, Vm, Func, Ph, f, R, Init, Tramp, Tconstant, Fault, Tfs, Tfe, Dr, V, I, Pin_0,
                             Pin_1):
    newACVoltageSource_1pJson = compLib['_newACVoltageSource_1p'];
    CnewACVoltageSource_1pJson = copy.deepcopy(newACVoltageSource_1pJson)
    newACVoltageSource_1p = Component(CnewACVoltageSource_1pJson)
    newACVoltageSource_1p.args['Name'] = Name
    newACVoltageSource_1p.args['Grnd'] = Grnd
    newACVoltageSource_1p.args['Vm'] = Vm
    newACVoltageSource_1p.args['Func'] = Func
    newACVoltageSource_1p.args['Ph'] = Ph
    newACVoltageSource_1p.args['f'] = f
    newACVoltageSource_1p.args['R'] = R
    newACVoltageSource_1p.args['Init'] = Init
    newACVoltageSource_1p.args['Tramp'] = Tramp
    newACVoltageSource_1p.args['Tconstant'] = Tconstant
    newACVoltageSource_1p.args['Fault'] = Fault
    newACVoltageSource_1p.args['Tfs'] = Tfs
    newACVoltageSource_1p.args['Tfe'] = Tfe
    newACVoltageSource_1p.args['Dr'] = Dr
    newACVoltageSource_1p.args['V'] = V
    newACVoltageSource_1p.args['I'] = I
    newACVoltageSource_1p.pins['0'] = Pin_0
    newACVoltageSource_1p.pins['1'] = Pin_1
    newACVoltageSource_1p.position['x'] = random.randint(100, 500)
    newACVoltageSource_1p.position['y'] = random.randint(100, 500)
    newACVoltageSource_1p.id = '_newACVoltageSource_1p'
    project.revision.implements.diagram.cells[newACVoltageSource_1p.id] = newACVoltageSource_1p
    print('单相交流电压源元件生成成功')
    # project.update(project);


# 创建接地点
def AddGND(Name, Pin):
    GNDJson = compLib['GND'];
    CGNDJson = copy.deepcopy(GNDJson)
    GND = Component(CGNDJson)
    GND.args['Name'] = Name
    GND.pins['0'] = Pin
    GND.position['x'] = random.randint(100, 500)
    GND.position['y'] = random.randint(100, 500)
    GND.id = 'GND'
    project.revision.implements.diagram.cells[GND.id] = GND
    print('接地点元件生成成功')
    # project.update(project);


# 创建电阻
def AddnewResistorRouter(Name, Dim, R, I, V, Pin_0, Pin_1):
    newResistorRouterJson = compLib['newResistorRouter'];
    CnewResistorRouterJson = copy.deepcopy(newResistorRouterJson)
    newResistorRouter = Component(CnewResistorRouterJson)
    newResistorRouter.args['Name'] = Name
    newResistorRouter.args['Dim'] = Dim
    newResistorRouter.args['R'] = R
    newResistorRouter.args['I'] = I
    newResistorRouter.args['V'] = V
    newResistorRouter.pins['0'] = Pin_0
    newResistorRouter.pins['1'] = Pin_1
    newResistorRouter.position['x'] = random.randint(100, 500)
    newResistorRouter.position['y'] = random.randint(100, 500)
    newResistorRouter.id = 'newResistorRouter'
    project.revision.implements.diagram.cells[newResistorRouter.id] = newResistorRouter
    print('电阻元件生成成功')
    # project.update(project);


# 创建电感
def AddnewInductorRouter(Name, Dim, L, NIM, I, V, Pin_0, Pin_1):
    newInductorRouterJson = compLib['newInductorRouter'];
    CnewInductorRouterJson = copy.deepcopy(newInductorRouterJson)
    newInductorRouter = Component(CnewInductorRouterJson)
    newInductorRouter.args['Name'] = Name
    newInductorRouter.args['Dim'] = Dim
    newInductorRouter.args['L'] = L
    newInductorRouter.args['NIM'] = NIM
    newInductorRouter.args['I'] = I
    newInductorRouter.args['V'] = V
    newInductorRouter.pins['0'] = Pin_0
    newInductorRouter.pins['1'] = Pin_1
    newInductorRouter.position['x'] = random.randint(100, 500)
    newInductorRouter.position['y'] = random.randint(100, 500)
    newInductorRouter.id = 'newInductorRouter'
    project.revision.implements.diagram.cells[newInductorRouter.id] = newInductorRouter
    print('电感元件生成成功')
    # project.update(project);


# 创建电容
def AddnewCapacitorRouter(Name, Dim, C, NIM, I, V, Pin_0, Pin_1):
    newCapacitorRouterJson = compLib['newCapacitorRouter'];
    CnewCapacitorRouterJson = copy.deepcopy(newCapacitorRouterJson)
    newCapacitorRouter = Component(CnewCapacitorRouterJson)
    newCapacitorRouter.args['Name'] = Name
    newCapacitorRouter.args['Dim'] = Dim
    newCapacitorRouter.args['C'] = C
    newCapacitorRouter.args['NIM'] = NIM
    newCapacitorRouter.args['I'] = I
    newCapacitorRouter.args['V'] = V
    newCapacitorRouter.pins['0'] = Pin_0
    newCapacitorRouter.pins['1'] = Pin_1
    newCapacitorRouter.position['x'] = random.randint(100, 500)
    newCapacitorRouter.position['y'] = random.randint(100, 500)
    newCapacitorRouter.id = 'newCapacitorRouter'
    project.revision.implements.diagram.cells[newCapacitorRouter.id] = newCapacitorRouter
    print('电感元件生成成功')
    # project.update(project);


# 创建电压表
def Add_NewVoltageMeter(Dim, V, Pin):
    _NewVoltageMeterJson = compLib['_NewVoltageMeter'];
    C_NewVoltageMeterJson = copy.deepcopy(_NewVoltageMeterJson)
    _NewVoltageMeter = Component(C_NewVoltageMeterJson)
    _NewVoltageMeter.args['Dim'] = Dim
    _NewVoltageMeter.args['V'] = V
    _NewVoltageMeter.pins['0'] = Pin
    _NewVoltageMeter.position['x'] = random.randint(100, 500)
    _NewVoltageMeter.position['y'] = random.randint(100, 500)
    _NewVoltageMeter.id = '_NewVoltageMeter'
    project.revision.implements.diagram.cells[_NewVoltageMeter.id] = _NewVoltageMeter
    print('电压表元件生成成功')
    # project.update(project);


# 创建输出通道
def Add_newChannel(Name, Dim, Pin):
    _newChannelJson = compLib['_newChannel'];
    C_newChannelJson = copy.deepcopy(_newChannelJson)
    _newChannel = Component(C_newChannelJson)
    _newChannel.args['Name'] = Name
    _newChannel.args['Dim'] = Dim
    _newChannel.pins['0'] = Pin
    _newChannel.position['x'] = random.randint(100, 500)
    _newChannel.position['y'] = random.randint(100, 500)
    _newChannel.id = '_newChannel' + str(Name)
    project.revision.implements.diagram.cells[_newChannel.id] = _newChannel
    print('输出通道元件生成成功')
    # project.update(project);


# 创建变压器（拓扑）
def AddTSF_Topo(id, Name, alias, disp_code, base_voltage, type, of_feeder, of_feeder_section, of_d_substation, model,
                rated_capacity, user_type, vip_amount, load_ratio, power_state, topo_island, vector_group, psrid,
                terminal, terminal2):
    TSF_TopoJson = compLib['TSF_Topo'];
    CTSF_TopoJson = copy.deepcopy(TSF_TopoJson)
    TSF_Topo = Component(CTSF_TopoJson)
    TSF_Topo.args['ID'] = id
    TSF_Topo.args['NAME'] = Name
    TSF_Topo.args['ALIAS'] = alias
    TSF_Topo.args['DISP_CODE'] = disp_code
    TSF_Topo.args['BASE_VOLTAGE'] = base_voltage
    TSF_Topo.args['TYPE'] = type
    TSF_Topo.args['OF_FEEDER'] = of_feeder
    TSF_Topo.args['OF_FEEDER_SECTION'] = of_feeder_section
    TSF_Topo.args['OF_D_SUBSTATION'] = of_d_substation
    TSF_Topo.args['MODEL'] = model
    TSF_Topo.args['RATED_CAPACITY'] = rated_capacity
    TSF_Topo.args['USER_TYPE'] = user_type
    TSF_Topo.args['VIP_AMOUNT'] = vip_amount
    TSF_Topo.args['LOAD_RATIO'] = load_ratio
    TSF_Topo.args['POWER_STATE'] = power_state
    TSF_Topo.args['TOPO_ISLAND'] = topo_island
    TSF_Topo.args['VECTOR_GROUP'] = vector_group
    TSF_Topo.pins['Terminal'] = terminal
    TSF_Topo.pins['Terminal2'] = terminal2
    TSF_Topo.position['x'] = random.randint(100, 500)
    TSF_Topo.position['y'] = random.randint(100, 500)
    TSF_Topo.id = id
    project.revision.implements.diagram.cells[TSF_Topo.id] = TSF_Topo
    print('变压器（拓扑）元件生成成功')


# AddBreaker('30500000-39674052','球山S421开关','断路器功能','FALSE','630','50000','PSRT9','30000000-113394359','AC00101','30500000-39674052_1','30500000-39674052_2','30000000-113394359_Lt1')
# AddnewACVoltageSource_1p('单相交流电压源','1','10','0','0','50','0','0','0.06','0.06','0','0.2','0.4','0.2','','','','A')
# AddGND('接地点','D')
# AddnewResistorRouter('电阻','0','10','','','','')
# AddnewInductorRouter('电感','0','0.01','1','','','B','C')
# AddnewCapacitorRouter('电容','0','5000','1','','','C','D')
# Add_NewVoltageMeter('1','#Vs','A')
# Add_newChannel('电压源端电压','','')
# Add_newChannel('123','','')
# AddTSF_Topo('canvas_0_1096_1','Trans1','100','$Bus_4_Vbase','$Bus_1_Vbase','50','0.01','0.01','0.05760','0','0','0.4','h1','Bus4','Bus1')
# AddTSF_Topo('canvas_0_1087_2','Trans2','100','$Bus_2_Vbase','$Bus_7_Vbase','50','0.01','0.01','0.06250','0','0','0.4','h2','Bus2','Bus7')
# AddTSF_Topo('canvas_0_1095_3','Trans3','100','$Bus_9_Vbase','$Bus_3_Vbase','50','0.01','0.01','0.05860','0','0','0.4','h3','Bus9','Bus3')

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")  # 多个客户端连接同样的地址

while True:
    event = Component_pb2.Component()
    socket.send(b"reply_string")
    response = socket.recv()
    event.ParseFromString(response)
    name = event.name.decode('gbk')
    alias = event.alias.decode('gbk')
    print(name, alias, event.component_type)
    if event.component_type == 0:
        AddTSF_Topo(event.id, name, alias, event.disp_code, event.base_voltage, event.type, event.of_feeder,
                    event.of_feeder_section, event.of_d_substation, event.model, event.rated_capacity, event.user_type,
                    event.vip_amount, event.load_ratio, event.power_state, event.topo_island, event.vector_group,
                    event.psrid, event.terminal, event.terminal2)
    if event.note == 1:
        break
# project.update(project)
# print(octal_name)
# Add_newChannel(event.id,'','')
# if yj.id == 1000 :
#    break
# project.update(project)

# project.update(project)
# while(1):
#     event = event_pb2.Event()
#     response = socket.recv()
#     event.ParseFromString(response)
#     print(event)
#     socket.send(b"reply_string")

# 八进制转中文测试
# byte_str = b"\344\270\252\344\272\272\350\265\204\346\226\231\345\215\241"
# byte_str_charset = chardet.detect(byte_str)  # 获取字节码编码格式
#
# byte_str = str(byte_str, byte_str_charset.get('encoding'))  # 将八进制字节流转化为字符串
# print(byte_str)
#
# # def Add_newBattery(m,Amax,Amin,Imax,Imin,K,Ki,Ki2,Kiv,Kv,PG0,QG0,Sbase,TC,TL,Ti,Tv,Vrate,Vt0,site):
# def Add_newBattery(m, Vt0):
#     _newBatteryJson = compLib['100kW-200kWh'];
#     C_newBatteryJson = copy.deepcopy(_newBatteryJson)
#     _newBattery = Component(C_newBatteryJson)
#     # _newBattery.args['Amax'] = Amax
#     # _newBattery.args['Amin'] = Amin
#     # _newBattery.args['Imax'] = Imax
#     # _newBattery.args['Imin'] = Imin
#     # _newBattery.args['Imax'] = Imax
#     # _newBattery.args['K'] = K
#     # _newBattery.args['Ki'] = Ki
#     # _newBattery.args['Ki2'] = Ki2
#     # _newBattery.args['Kiv'] = Kiv
#     # _newBattery.args['Kv'] = Kv
#     # _newBattery.args['PG0'] = PG0
#     # _newBattery.args['QG0'] = QG0
#     # _newBattery.args['Sbase'] = Sbase
#     # _newBattery.args['TC'] = TC
#     # _newBattery.args['TL'] = TL
#     # _newBattery.args['Ti'] = Ti
#     # _newBattery.args['Tv'] = Tv
#     # _newBattery.args['Vrate'] = Vrate
#     _newBattery.args['Vt0'] = Vt0
#     # _newBattery.args['site'] = site
#     _newBattery.id = 'component_100_k_w_200_k_wh_'+str(m)
#     project.revision.implements.diagram.cells[_newBattery.id] = _newBattery
#     print('蓄电池元件生成成功')
#
# #def Add_newWind(m,FaultDropRatio,FaultEndTime,FaultSet,FaultStartTime,Pref,Qref,UnitTest,Vpcc,WT_Num):
# def Add_newWind(m,  Pref,  Vpcc, WT_Num):
#     _newWindJson = compLib['GW_mask_single_for_AP2'];
#     C_newWindJson = copy.deepcopy(_newWindJson)
#     _newWind = Component(C_newWindJson)
#     # _newWind.args['FaultDropRatio'] = FaultDropRatio
#     # _newWind.args['FaultEndTime'] = FaultEndTime
#     # _newWind.args['FaultSet'] = FaultSet
#     # _newWind.args['FaultStartTime'] = FaultStartTime
#     _newWind.args['Pref'] = Pref
#     # _newWind.args['Qref'] = Qref
#     # _newWind.args['UnitTest'] = UnitTest
#     _newWind.args['Vpcc'] = Vpcc
#     _newWind.args['WT_Num'] = WT_Num
#     _newWind.id = 'component_gw_mask_single_for_ap_2_'+str(m)
#     project.revision.implements.diagram.cells[_newWind.id] = _newWind
#     print('风机元件生成成功')
#
# # def Add_newPV(m,Name,Amax,Amin,Im,Imax,Imin,Isc,Ki,Ki2,Kiv,Kv,PG0,QG0,Sbase,Smax,Smin,T,TC,TL,Ti,Tv,UnitTest,Vm,Voc,Vrate,Vt0,site):
# def Add_newPV(m, Name,Sbase, Vt0):
#     _newPVJson = compLib['PV'];
#     C_newPVJson = copy.deepcopy(_newPVJson)
#     _newPV = Component(C_newPVJson)
#     # _newPV.args['Amax'] = Amax
#     # _newPV.args['Amin'] = Amin
#     # _newPV.args['Imax'] = Imax
#     # _newPV.args['Imin'] = Imin
#     # _newPV.args['Imax'] = Imax
#     # _newPV.args['Im'] = Im
#     # _newPV.args['Ki'] = Ki
#     # _newPV.args['Ki2'] = Ki2
#     # _newPV.args['Kiv'] = Kiv
#     # _newPV.args['Kv'] = Kv
#     # _newPV.args['PG0'] = PG0
#     # _newPV.args['QG0'] = QG0
#     _newPV.args['Sbase'] = Sbase
#     # _newPV.args['TC'] = TC
#     # _newPV.args['TL'] = TL
#     # _newPV.args['Ti'] = Ti
#     # _newPV.args['Tv'] = Tv
#     # _newPV.args['Vrate'] = Vrate
#     _newPV.args['Vt0'] = Vt0
#     # _newPV.args['site'] = site
#     # _newPV.args['Isc'] = Isc
#     # _newPV.args['Smax'] = Smax
#     # _newPV.args['Smin'] = Smin
#     # _newPV.args['T'] = T
#     # _newPV.args['UnitTest'] = UnitTest
#     # _newPV.args['Vm'] = Vm
#     # _newPV.args['Voc'] = Voc
#     _newPV.args['Name'] = Name
#     _newPV.id = 'component_pv_'+str(m)
#     project.revision.implements.diagram.cells[_newPV.id] = _newPV
#     print('光伏元件生成成功')
#
#
# for i in range(90):
#     Vt0_1 = '0.9981'+str(random.randint(100, 999))
#     Add_newBattery(i+3,Vt0_1)
#
# for x in range(100):
#     Pref = str(random.randint(0, 1)) +'.'+str(random.randint(1, 9))
#     WT_Num = str(random.randint(1, 3))
#     Vpcc = '0.69'
#     Add_newWind(x+3,Pref,Vpcc,WT_Num)
#
# for y in range(110):
#     Vt0_2 = str(random.uniform(0.99, 0.999))
#     first_name = ["德", "体", "智", "行", "文", "略", "仪", "恒", "雅", "杨", "慧", "马", "高", "殷", "秀", "机",
#                   "常"]
#     second_name = ["伟", "华", "国", "洋", "刚", "里", "民", "牧", "陆", "路", "昕", "鑫", "兵", "硕", "志",
#                    "峰", "磊", "雷", "文", "浩", "光", "超", "军", "达"]
#     name = str(random.choice(first_name) + random.choice(second_name)) + '楼顶分散光伏'
#     Sbase = '0.0'+str(random.randint(111,999))
#     Add_newPV(y+5,name,Sbase,Vt0_2)
#
# project.update(project)
