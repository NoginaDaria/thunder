import pytest
from lightning import Trainer

from thunder.callbacks import FailOnInterrupt
from lightning.pytorch.demos.boring_classes import BoringModel


class FailureModel(BoringModel):
    def __init__(self, exception: BaseException):
        super().__init__()
        self.exc = exception

    def training_step(self, batch, batch_idx):
        if batch_idx > 0:
            raise self.exc


class NewKeyboardInterrupt(KeyboardInterrupt):
    pass


@pytest.mark.parametrize(
    "exception, behaviour",
    [
        (RuntimeError, pytest.raises(RuntimeError)),
        (ValueError, pytest.raises(ValueError)),
        (KeyboardInterrupt, pytest.raises(RuntimeError, match="Finished run on KeyboardInterrupt")),
        (NewKeyboardInterrupt, pytest.raises(RuntimeError, match="Finished run on KeyboardInterrupt")),
    ],
)
def test_failing(exception, behaviour, tmpdir):
    module = FailureModel(exception)
    trainer = Trainer(default_root_dir=tmpdir, max_epochs=2, callbacks=[FailOnInterrupt()])

    with behaviour:
        trainer.fit(module)
        assert False, "Test hasn't failed on trainer.fit"
        trainer.test(module)
