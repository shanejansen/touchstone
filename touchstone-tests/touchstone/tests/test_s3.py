from touchstone.lib.touchstone_test import TouchstoneTest


class BucketCreated(TouchstoneTest):
    def given(self) -> object:
        return 'foo'

    def when(self, given) -> object:
        self.mocks.s3.setup().create_bucket(given)
        return None

    def then(self, given, result) -> bool:
        return self.mocks.s3.verify().bucket_exists(given)


class PutObjectExists(TouchstoneTest):
    BUCKET_NAME = 'foo'
    OBJECT_NAME = 'bar'

    def given(self) -> object:
        self.mocks.s3.setup().create_bucket(self.BUCKET_NAME)
        return bytes('buzz', encoding='utf-8')

    def when(self, given) -> object:
        self.mocks.s3.setup().put_object(self.BUCKET_NAME, self.OBJECT_NAME, given)
        return None

    def then(self, given, result) -> bool:
        return self.mocks.s3.verify().object_exists(self.BUCKET_NAME, self.OBJECT_NAME)


class PutObjectMatches(TouchstoneTest):
    BUCKET_NAME = 'foo'
    OBJECT_NAME = 'bar'

    def given(self) -> object:
        self.mocks.s3.setup().create_bucket(self.BUCKET_NAME)
        return bytes('buzz', encoding='utf-8')

    def when(self, given) -> object:
        self.mocks.s3.setup().put_object(self.BUCKET_NAME, self.OBJECT_NAME, given)
        return None

    def then(self, given, result) -> bool:
        return self.mocks.s3.verify().object_matches(self.BUCKET_NAME, self.OBJECT_NAME, given)
