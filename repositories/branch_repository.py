from database import db
from models.branch import Branch
from repositories.base_repository import BaseRepository


class BranchRepository(BaseRepository):
    def __init__(self):
        super().__init__(Branch)