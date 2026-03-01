from hydra.database.unit_of_work import UnitOfWork


class BaseService:
    uow: UnitOfWork

    def __init__(self, unit_of_work: UnitOfWork):
        self.uow = unit_of_work
