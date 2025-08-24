# -*- coding: utf-8 -*-
# Jcen

from .action import *


BehaviorTree.register_node(CreateBox)
BehaviorTree.register_node(UsdCreateInMemory)
BehaviorTree.register_node(UsdCreateToFile)
BehaviorTree.register_node(SetMateData)
BehaviorTree.register_node(SetCustomMetaData)
BehaviorTree.register_node(SetUsdPrim)
BehaviorTree.register_node(SetPayloads)
BehaviorTree.register_node(UsdSave)

