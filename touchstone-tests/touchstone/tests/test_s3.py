from touchstone.lib.touchstone_test import TouchstoneTest


class BucketCreated(TouchstoneTest):
    def given(self) -> object:
        return 'foo'

    def when(self, given) -> object:
        self.mocks.s3.setup.create_bucket(given)
        return None

    def then(self, given, result) -> bool:
        return self.mocks.s3.verify.bucket_exists(given)


class PutObjectExists(TouchstoneTest):
    def given(self) -> object:
        return {
            'bucket_name': 'foo',
            'object_name': 'bar',
            'data': 'buzz'
        }

    def when(self, given) -> object:
        self.mocks.s3.setup.put_object(given['bucket_name'], given['object_name'],
                                       bytes(given['data'], encoding='utf-8'))
        return None

    def then(self, given, result) -> bool:
        return self.mocks.s3.verify.object_exists(given['bucket_name'], given['object_name'])
