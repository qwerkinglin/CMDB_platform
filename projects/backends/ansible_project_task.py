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
from CMDB_platform import settings

# Create a callback object so we can capture the output
class ResultsCollector(CallbackBase):

    def __init__(self, display=None):
        super(ResultsCollector, self).__init__(display)
        self.results = []

    def _new_play(self, play):
        return {
            'play': {
                'name': play.name,
                'id': str(play._uuid)
            },
            'tasks': []
        }

    def _new_task(self, task):
        return {
            'task': {
                'name': task.name,
                'id': str(task._uuid)
            },
            'hosts': {}
        }

    def v2_playbook_on_play_start(self, play):
        self.results.append(self._new_play(play))

    def v2_playbook_on_task_start(self, task, is_conditional):
        self.results[-1]['tasks'].append(self._new_task(task))

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        self.results[-1]['tasks'][-1]['hosts'][host.name] = result._result

    def v2_playbook_on_stats(self, stats):
        """Display info about playbook statistics"""

        hosts = sorted(stats.processed.keys())

        summary = {}
        for h in hosts:
            s = stats.summarize(h)
            summary[h] = s

        output = {
            'plays': self.results,
            'stats': summary
        }
        print(json.dumps(output, indent=4, sort_keys=True))
    v2_runner_on_failed = v2_runner_on_ok
    v2_runner_on_unreachable = v2_runner_on_ok
    v2_runner_on_skipped = v2_runner_on_ok

def main(host_list,module,args):
    Options = namedtuple('Options', ['connection','module_path', 'forks', 'remote_user',
            'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
            'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])

    # initialize needed objects
    variable_manager = VariableManager()
    loader = DataLoader()
    options = Options(connection='smart', module_path='xxx', forks=50,
            remote_user='root', private_key_file=settings.Private_Key, ssh_common_args=None, ssh_extra_args=None,
            sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
            become_user=None, verbosity=None, check=False)

    passwords = dict(sshpass=None, becomepass=None)

    # create inventory and pass to var manager
    inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=host_list)
    variable_manager.set_inventory(inventory)

    # create play with tasks
    play_source =  dict(
            name = "Ansible Play",
            hosts = host_list,
            gather_facts = 'no',
            tasks = [ dict(action=dict(module=module, args=args)) ]
        )
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    # actually run it
    tqm = None
    callback = ResultsCollector()
    try:
        tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=options,
                passwords=passwords,
            )
        tqm._stdout_callback = callback
        tqm.run(play)
        return callback.results[0]['tasks'][0]['hosts']

    finally:
        if tqm is not None:
            tqm.cleanup()

if __name__ == '__main__':          #测试用
    host_list = []
    module = 'raw'
    args = 'ifconfig'
    main(host_list,module,args)
