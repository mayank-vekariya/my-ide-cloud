"""The liveness endpoint must work without invoking cloud deployment."""
import unittest
from unittest.mock import patch

from app import create_app


class HealthTest(unittest.TestCase):
    def test_liveness_does_not_call_cloud(self):
        application = create_app()
        application.config['TESTING'] = True
        with patch('app.main.routes.run_command') as run_command:
            response = application.test_client().get('/healthz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'status': 'ok', 'service': 'code-server-dashboard'})
        run_command.assert_not_called()


if __name__ == '__main__':
    unittest.main()
