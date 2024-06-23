import os
import sys
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from concurrent import futures

import grpc
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from src.data.history import PostgresHistory
from src.dep.postgres import get_postgres
from src.grpc_llm import llm_service_pb2, llm_service_pb2_grpc
from src.services.llm_service import LLMConversationService
from src.services.text_bot_service import TextSerivce


class LLMServicer(llm_service_pb2_grpc.LLMServicer):
    def __init__(self):
        self.text_service = TextSerivce()

    def PredictConversation(self, request, context):
        input_text: str = request.input_text
        chat_id: int = request.chat_id
        user_id: str = request.user_id
        timestamp: int = request.timestamp
        msg_date = datetime.fromtimestamp(timestamp / 1e3)

        prediction = self.text_service.text_chat_history(
            chat_id, user_id, input_text, msg_date
        )

        return llm_service_pb2.PredictResponse(prediction=prediction)

    def PredictMessage(self, request, context):
        input_text: str = request.input_text

        prediction = self.text_service.single_message_predict(input_text)

        return llm_service_pb2.PredictResponse(prediction=prediction)

    def PredictRAG(self, request, context):
        return llm_service_pb2.PredictResponse(prediction='')

    def PredictAgent(self, request, context):
        return llm_service_pb2.PredictResponse(prediction=prediction)

    def Summary(self, request, context):
        chat_id: int = request.chat_id
        user_id: str = request.user_id
        prediction = self.text_service.history_summary(chat_id, user_id)

        return llm_service_pb2.PredictResponse(prediction=prediction)

    def GatherMessage(self, request, context):
        input_text: str = request.input_text
        chat_id: int = request.chat_id
        user_id: str = request.user_id
        timestamp: int = request.timestamp
        msg_date = datetime.fromtimestamp(timestamp / 1e3)

        self.text_service.collect_chat_history(chat_id, user_id, input_text, msg_date)
        return llm_service_pb2.empty()

    def ClearHistory(self, request, context):
        chat_id: int = request.chat_id
        user_id: str = request.user_id

        self.text_service.drop_context(chat_id, user_id)
        return llm_service_pb2.empty()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    llm_service_pb2_grpc.add_LLMServicer_to_server(LLMServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
