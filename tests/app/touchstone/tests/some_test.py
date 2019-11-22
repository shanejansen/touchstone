# import json
#
# from touchstone_test import TouchstoneTest
#
#
# class SomeTest(TouchstoneTest):
#     def name(self) -> str:
#         return 'Some Test'
#
#     def given(self, test_context):
#         response = {
#             'foo': 'bar'
#         }
#         test_context.mocks.http.setup().get('/foo', json.dumps(response))
#
#     def when(self, test_context):
#         return 1
#
#     def then(self, test_context, test_result) -> bool:
#         return test_result == 1
