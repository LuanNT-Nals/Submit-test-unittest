import csv
import time

from abc import ABC, abstractmethod
from typing import List, Any


class Order:
	def __init__(self, id: int, type: str, amount: float, flag: bool):
		self.id = id
		self.type = type
		self.amount = amount
		self.flag = flag
		self.status = 'new'
		self.priority = 'low'


class APIResponse:
	def __init__(self, status: str, data: Any):
		self.status = status
		self.data = data


class APIException(Exception):
	pass


class DatabaseException(Exception):
	pass


class DatabaseService(ABC):
	@abstractmethod
	def get_orders_by_user(self, user_id: int) -> List[Order]:
		pass

	@abstractmethod
	def update_order_status(self, order_id: int, status: str, priority: str) -> bool:
		pass


class APIClient(ABC):
	@abstractmethod
	def call_api(self, order_id: int) -> APIResponse:
		pass


class OrderExporter:
	def export_order_to_csv(self, order: Order, user_id: int) -> str:
		csv_file = f'orders_type_A_{user_id}_{int(time.time())}.csv'
		try:
			with open(csv_file, 'w', newline='') as file_handle:
				writer = csv.writer(file_handle)
				writer.writerow(['ID', 'Type', 'Amount', 'Flag', 'Status', 'Priority'])
				writer.writerow([
					order.id,
					order.type,
					order.amount,
					str(order.flag).lower(),
					order.status,
					order.priority
				])
				if order.amount > 150:
					writer.writerow(['', '', '', '', 'Note', 'High value order'])
			return 'exported'
		except IOError:
			return 'export_failed'


class OrderTypeAHandler:
	def __init__(self, exporter: OrderExporter):
		self.exporter = exporter

	def handle(self, order: Order, user_id: int) -> str:
		return self.exporter.export_order_to_csv(order, user_id)


class OrderTypeBHandler:
	def __init__(self, api_client: APIClient):
		self.api_client = api_client

	def handle(self, order: Order) -> str:
		try:
			api_response = self.api_client.call_api(order.id)
			if api_response.status == 'success':
				if api_response.data >= 50 and order.amount < 100:
					return 'processed'
				elif api_response.data < 50 or order.flag:
					return 'pending'
				return 'error'
			return 'api_error'
		except APIException:
			return 'api_failure'


class OrderTypeCHandler:
	def handle(self, order: Order) -> str:
		return 'completed' if order.flag else 'in_progress'


class OrderPriorityManager:
	def determine_priority(self, order: Order) -> str:
		return 'high' if order.amount > 200 else 'low'


class OrderProcessingService:
	def __init__(
		self,
		db_service: DatabaseService,
		api_client: APIClient,
		order_exporter: OrderExporter = None
	):
		self.db_service = db_service
		self.api_client = api_client
		self.order_exporter = order_exporter or OrderExporter()
		self.type_a_handler = OrderTypeAHandler(self.order_exporter)
		self.type_b_handler = OrderTypeBHandler(api_client)
		self.type_c_handler = OrderTypeCHandler()
		self.priority_manager = OrderPriorityManager()

	def _process_order(self, order: Order, user_id: int) -> None:
		if order.type == 'A':
			order.status = self.type_a_handler.handle(order, user_id)
		elif order.type == 'B':
			order.status = self.type_b_handler.handle(order)
		elif order.type == 'C':
			order.status = self.type_c_handler.handle(order)
		else:
			order.status = 'unknown_type'

		order.priority = self.priority_manager.determine_priority(order)

		try:
			self.db_service.update_order_status(order.id, order.status, order.priority)
		except DatabaseException:
			order.status = 'db_error'

	def process_orders(self, user_id: int) -> bool:
		try:
			orders = self.db_service.get_orders_by_user(user_id)
			if not orders:
				return False

			for order in orders:
				self._process_order(order, user_id)
			return True
		except Exception:
			return False