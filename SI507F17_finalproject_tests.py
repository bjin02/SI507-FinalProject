import unittest
from SI507F17_finalproject import *

class TestHelperFunctions(unittest.TestCase):
    def setUp(self):
        self.infoData = {"response":{"blog":{"followed":"true","total_posts":"5","title":"test","url":"test.com","ask_page_title":"test","name":"123"}}}
        self.postData = {"response":{"posts":[{"date":"123","summary":"123","format":"123","short_url":"123","can_like":"true","can_reply":"true","type":"test","photos":[{"original_size":{"url":"test.com"}}]},{"date":"1234","summary":"1234","format":"1234","short_url":"1234","can_like":"true","can_reply":"true","type":"test","photos":[{"original_size":{"url":"test.com"}}]}]}}

    def testGenerate_model_instances(self):
        info, posts = generate_model_instances(self.infoData, self.postData)
        self.assertEqual(info.title, "test")
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0].date, "123")
        self.assertEqual(posts[1].date, "1234")
        return

class TestFiles(unittest.TestCase):
    def setUp(self):
        self.plot = open("temp-plot.html")
        self.creds = open("creds.json", encoding='utf-8')
        self.cache_contents = open("cache_contents.json", encoding='utf-8')

    def testPlotFileExists(self):
        self.assertTrue(self.plot.read())

    def testJsonFileExists(self):
        self.assertTrue(self.creds.read())
        self.assertTrue(self.cache_contents.read())

    def tearDown(self):
        self.plot.close()
        self.creds.close()
        self.cache_contents.close()

class TestTumblrAPI(unittest.TestCase):
    def testHasCacheExpired(self):
        isExpired = has_cache_expired("2017-10-09 00:08:59.893171", 1)
        self.assertTrue(isExpired, True)
        return

    def testGetFromCache(self):
        creds_data = get_from_cache("/INFO", CREDS_DICTION)
        self.assertTrue(type(creds_data) is list)

        data = get_from_cache('HTTPS://API.TUMBLR.COM/V2/BLOG/?API_/POSTS_BLOG-IDENTIFIER_VINBEIGIE', CACHE_DICTION)
        self.assertTrue(type(data) is dict)
        return

    def testCreateRequestIdentifier(self):
        identifier = create_request_identifier('https://api.tumblr.com/v2/blog/', {'blog-identifier': 'vinbeigie', 'api': '/info'})
        self.assertEqual(identifier, 'HTTPS://API.TUMBLR.COM/V2/BLOG/?API_/INFO_BLOG-IDENTIFIER_VINBEIGIE')
        return

    def testGetCachedDataFrom_api(self):
        data = get_data_from_api('https://api.tumblr.com/v2/blog/', {'api': '/info', 'blog-identifier': 'vinbeigie'})
        self.assertTrue(type(data) is dict)
        return

    def testGetCachedTokenFromService(self):
        token = get_tokens_from_service("/INFO")
        self.assertTrue(type(token) is list)
        return

class TestModels(unittest.TestCase):
    def setUp(self):
        infoData = {"response":{"blog":{"followed":"true","total_posts":"5","title":"test","url":"test.com","ask_page_title":"test","name":"123"}}}
        postData = {"date":"123","summary":"123","format":"123","short_url":"123","can_like":"true","can_reply":"true","type":"test","photos":[{"original_size":{"url":"test.com"}}]}
        self.info = Info(infoData)
        self.post = Post(postData, self.info.id)

    def testInfoConstructor(self):
        self.assertIsInstance(self.info.id, int)
        self.assertEqual(self.info.ask_page_title, "test")
        self.assertEqual(self.info.followed, True)
        self.assertEqual(self.info.name, "123")
        self.assertEqual(self.info.title, "test")
        self.assertEqual(self.info.url, "test.com")

    def testPostConstructor(self):
        self.assertIsInstance(self.post.id, int)
        self.assertEqual(self.post.date, "123")
        self.assertEqual(self.post.summary, "123")
        self.assertEqual(self.post.format, "123")
        self.assertEqual(self.post.short_url, "123")
        self.assertEqual(self.post.can_like, True)
        self.assertEqual(self.post.can_reply, True)
        self.assertEqual(self.post.type, "test")
        self.assertEqual(self.post.image, "test.com")

    def testInfoIdInPost(self):
        self.assertEqual(self.info.id, self.post.info_id)

    def testInfoRepr(self):
        self.assertEqual(repr(self.info), "Blog Info Data Name:123\n Url:test.com Title:test\n Ask Page Title:test\n Total Posts:5\n Is Followed:True")

    def testPostRepr(self):
        self.assertEqual(repr(self.post), "Post Data Summary:123\n Creaated Date:123\n Fomrat:123\n Short_URL:123\n Can Like:True\n Can Reply:True\n Type:test")

    def testInfoContains(self):
        self.assertTrue(self.info.__contains__("123"))
        self.assertTrue(self.info.__contains__("test"))
        self.assertFalse(self.info.__contains__("890"))

    def testPostContains(self):
        self.assertTrue(self.post.__contains__("123"))
        self.assertFalse(self.post.__contains__("890"))

if __name__ == "__main__":
    unittest.main(verbosity=2)
