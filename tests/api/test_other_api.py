from db_requester.models import AccountTransactionTemplate
from utils.data_generator import DataGenerator
import pytest

class TestOtherAPI:
    def test_accounts_transaction_template(self, db_session):
        stan = AccountTransactionTemplate(user=f"Stan_{DataGenerator.generate_random_str(10)}", balance=1000)
        bob = AccountTransactionTemplate(user=f"Bob_{DataGenerator.generate_random_str(10)}", balance=500)

        # Добавляем записи в сессию
        db_session.add_all([stan, bob])
        db_session.commit()

        def transfer_money(session, from_account, to_account, amount):
            # пример функции выполняющей транзакцию
            # представим что она написана на стороне тестируемого сервиса
            # и вызывая метод transfer_money, мы какбудтобы делем запрос в api_manager.movies_api.transfer_money
            """
            Переводит деньги с одного счета на другой.
            :param session: Сессия SQLAlchemy.
            :param from_account_id: ID счета, с которого списываются деньги.
            :param to_account_id: ID счета, на который зачисляются деньги.
            :param amount: Сумма перевода.
            """
            # Получаем счета
            from_account = session.query(AccountTransactionTemplate).filter(AccountTransactionTemplate.user == from_account.user).first()
            to_account = session.query(AccountTransactionTemplate).filter(AccountTransactionTemplate.user == to_account.user).first()

            if from_account.balance < amount:
                raise ValueError("Недостаточно средств на счете")

            # Выполняем перевод
            from_account.balance -= amount
            to_account.balance += amount
            # Сохраняем изменения
            session.commit()

        assert stan.balance == 1000
        assert bob.balance == 500

        # Проверяет, что произошла ожидаемая ошибка
        with pytest.raises(ValueError, match="Недостаточно средств на счете"):
            transfer_money(db_session, bob, stan, 600)

        # Откатывает изменения в БД и восстанавливает рабочее состояние сессии после ошибки
        db_session.rollback()

        stan_from_db = db_session.query(AccountTransactionTemplate).filter(AccountTransactionTemplate.user == stan.user).first()
        bob_from_db = db_session.query(AccountTransactionTemplate).filter(AccountTransactionTemplate.user == bob.user).first()

        assert stan_from_db.balance == 1000
        assert bob_from_db.balance == 500

        db_session.delete(stan)
        db_session.delete(bob)
        db_session.commit()
