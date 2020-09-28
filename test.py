from api import app
import unittest,json

class APITest(unittest.TestCase):
    def test_login_route(self):
        tester = app.test_client(self)
        response = tester.get('/login',content_type='html/text')
        self.assertEqual(response.status_code,200)
        
    def test_login_route_content(self):
        tester = app.test_client(self)
        response = tester.get('/login',content_type='html/text')
        self.assertTrue(b'Jobsity Chat'in response.data)
    
    def test_signup_route(self):
        tester = app.test_client(self)
        response = tester.get('/signup',content_type='html/text')
        self.assertEqual(response.status_code,200)
        
    def test_signup_route_content(self):
        tester = app.test_client(self)
        response = tester.get('/signup',content_type='html/text')
        self.assertTrue(b'Create Account'in response.data)

    def test_rooms_route(self):
        tester = app.test_client(self)
        response = tester.get('/rooms',content_type='html/text')
        self.assertEqual(response.status_code,302)

    def test_message_content(self):
        tester = app.test_client(self)
        response = tester.post('/message',data=json.dumps(dict(username='StockBot',room='engineering',secret="jobsitystockbotkey",message="Bot Test")))
        self.assertEqual(response.status_code,401)
    
   
  
if __name__ == '__main__':
    unittest.main()