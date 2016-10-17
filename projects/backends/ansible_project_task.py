#^v^! coding: utf-8 ^v^!
__author__ = 'Alex hao'

import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

# class ResultCallback(CallbackBase):       #自定义回调函数
#     """A sample callback plugin used for performing an action as results come in
#
#     If you want to collect all results into a single object for processing at
#     the end of the execution, look into utilizing the ``json`` callback plugin
#     or writing your own custom callback plugin
#     """
#     def v2_runner_on_ok(self, result, **kwargs):
#         """Print a json representation of the result
#
#         This method could store the result in an instance attribute for retrieval later
#         """
#         host = result._host
#         #print json.dumps({host.name: result._result["stdout"]}, indent=4)

def ansible_runner(hostlist,module,args):
    Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check'])
    # initialize needed objects
    variable_manager = VariableManager()
    loader = DataLoader()
    options = Options(connection='paramiko', module_path="xxx",  forks=50, become=None, become_method=None, become_user=None, check=False)
    passwords = dict(vault_pass='secret')

    # Instantiate our ResultCallback for handling results as they come in
    #results_callback = ResultCallback()    #自定义回调函数

    # create inventory and pass to var manager
    inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=hostlist)
    variable_manager.set_inventory(inventory)

    # create play with tasks
    play_source =  dict(
            name = "Ansible Play",
            hosts = hostlist,
            gather_facts = 'no',
            tasks = [
                dict(action=dict(module=module, args=args))
             ]
        )
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    # actually run it
    tqm = None
    try:
        tqm = TaskQueueManager(
                  inventory=inventory,
                  variable_manager=variable_manager,
                  loader=loader,
                  options=options,
                  passwords=passwords,
                  stdout_callback="minimal",
              )
        result = tqm.run(play)
        return result
    finally:
        if tqm is not None:
            tqm.cleanup()


