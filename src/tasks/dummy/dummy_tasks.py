from lib.task import BaseTask


class DummyAdd(BaseTask):

    required_params = ("to_add", )

    def run_with_params(self):

        return sum(self.params["to_add"])
