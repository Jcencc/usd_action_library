# -*- coding: utf-8 -*-
# Jcen

from behavior_tree.core import (
    Action, Blackboard, Status, Inverter, Condition, Repeater, UntilFail, BehaviorTree
)
import logging

# try:
#     from pxr import Usd, Sdf
# except:
#     pass

from pxr import Usd, Sdf

# test Action
class CreateBox(Action):
    def execute(self, blackboard: Blackboard) -> Status:
        return Status.SUCCESS

#

class UsdCreateInMemory(Action):
    info = """"""

    def execute(self, blackboard: Blackboard) -> Status:
        stage = Usd.Stage.CreateInMemory()
        blackboard.set("stage", stage)
        return Status.SUCCESS


class UsdCreateToFile(Action):
    info = """"""

    def execute(self, blackboard: Blackboard) -> Status:
        if not blackboard.get('usdpath'):
            logging.error('There is no usdpath key')
            return Status.FAILURE
        stage = Usd.Stage.CreateNew(blackboard.get('usdpath'))
        blackboard.get("stage", stage)
        return Status.SUCCESS


class SetMateData(Action):
    info = """"""

    def execute(self, blackboard: Blackboard) -> Status:
        super().set_blackboard()
        if not blackboard.get('stage') or not blackboard.get('set_usd_metadata'):
            logging.error('No stage object')
            return Status.FAILURE
        stage = blackboard.get('stage')
        metadata = blackboard.get('set_usd_metadata', {})
        for key, value in eval(metadata).items():
            stage.SetMetadata(key, value)

        return Status.SUCCESS


class SetCustomMetaData(Action):
    def execute(self, blackboard: Blackboard) -> Status:
        if not blackboard.get('set_usd_custom_metadata') or not blackboard.get('stage'):
            logging.error('There is no set_usd_custom_metadata key or No stage object')
            return Status.FAILURE
        stage = blackboard.get('stage')
        metadata = blackboard.get('set_usd_custom_metadata', {})
        for key, value in metadata.items():
            stage.SetMetadata(key, value)
        return Status.SUCCESS


class SetUsdPrim(Action):
    def execute(self, blackboard: Blackboard) -> Status:
        super().set_blackboard()

        if not blackboard.get('stage') or not blackboard.get('prim') or not blackboard.get('prim_type'):
            logging.error('There is no prim key or No stage object')
            return Status.FAILURE
        stage = blackboard.get('stage')
        prim_type = blackboard.get('prim_type')
        prim = blackboard.get('prim')
        prims = blackboard.get('prims', [])
        blackboard.set('prims', prims)
        for i in range(blackboard.get('primdepth', 1)):
            if not prims:
                prims.append(prim)
                stage.DefinePrim(prim, prim_type)
            else:
                parent_prim_path = ''.join(prims[:-1])
                stage.DefinePrim(parent_prim_path, prim_type)
                prims.append(prim)
        return Status.SUCCESS


class SetPayloads(Action):
    def execute(self, blackboard: Blackboard) -> Status:
        super().set_blackboard()
        if not blackboard.get('stage') or not blackboard.get('prim') or not blackboard.get('paylodfilepath'):
            logging.error('%s %s %s' % (blackboard.get('stage'), blackboard.get('prim'), blackboard.get('paylodfilepath')))
            logging.error('There is no prim key or There is no paylodfilepath key or No stage object')
            return Status.FAILURE
        payload_usda_path = blackboard.get('paylodfilepath')
        prim_path = blackboard.get('prim')
        stage = blackboard.get('stage')
        prim = stage.GetPrimAtPath(blackboard.get('prim'))
        if not prim.IsValid():
            logging.error(f"not prim: {prim_path}")
            return Status.FAILURE

        primPath = ''
        if blackboard.get('paylodprimpath'):
            primPath = blackboard.get('paylodprimpath')
        payload_path = Sdf.Payload(
            assetPath=payload_usda_path,
            primPath=primPath
        )

        payloads = prim.GetPayloads()
        payloads.AddPayload(payload_path)
        return Status.SUCCESS


class UsdSave(Action):
    info = """"""

    def execute(self, blackboard: Blackboard) -> Status:
        if not blackboard.get('stage') or not blackboard.get('usdpath'):
            logging.error('No stage object or No usdpath key ')
            return Status.FAILURE
        stage = blackboard.get('stage')
        stage.Export(blackboard.get('usdpath'))
        return Status.SUCCESS


