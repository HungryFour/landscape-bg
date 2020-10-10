from services.base_service import BaseService
from models.employee_model import EmployeeModel


class EmployeeService(BaseService):
    def __init__(self, *args, **kwargs):
        super(EmployeeService, self).__init__(*args, **kwargs)

    def create_employee(self, creator_id, name, avatar, title1, title2, production):
        employee = EmployeeModel(
            creator_id=creator_id,
            avatar=avatar,
            name=name,
            title1=title1,
            title2=title2,
            production=production
        )
        with self.session_scope() as session:
            session.add(employee)
            session.commit()
        return True

    def employees(self):
        with self.session_scope() as session:
            employeeList = session.query(EmployeeModel).all()
        return employeeList

    def update_employee(self, employee_id, name, avatar, title1, title2, production):
        with self.session_scope() as session:
            employee = session.query(EmployeeModel) \
                .filter(EmployeeModel.id == employee_id).first()

            if not employee:
                self.return_error(20002)

            employee.name = name
            employee.avatar = avatar
            employee.title1 = title1
            employee.title2 = title2
            employee.production = production

            session.commit()
        return True

    def remove_employee(self, employee_id):
        with self.session_scope() as session:
            resource = session.query(EmployeeModel) \
                .filter(EmployeeModel.id == employee_id).first()
            if not resource:
                self.return_error(20002)
            session.delete(resource)
            session.commit()
        return True
