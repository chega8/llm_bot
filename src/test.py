import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime

import pytest
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from src.data.history import FileChatMessageHistory
from src.data.utils import merge_all_files
from src.dep.mongo import get_mongo

f = FileChatMessageHistory("data/history", 566572635)
print(f.messages)
