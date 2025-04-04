from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

class GithubApiClient(object):
    GITHUB_API_URL = 'https://api.github.com/graphql'
    USER_AGENT = 'WMDE Github API Client'
    def __init__(self, token):
        self.token = token

    def get_changes_data(self, repository, since_date=None):
        transport = RequestsHTTPTransport(url=self.GITHUB_API_URL, headers={'Authorization': 'bearer %s' % self.token, 'User-Agent': self.USER_AGENT})
        client = Client(transport=transport, fetch_schema_from_transport=True)

        result = []

        should_fetch_next_batch = True
        after_cursor = 'null'
        while should_fetch_next_batch:

            query = gql(
                """
                {
      search(
        query: "repo:%s type:pr is:merged created:>=%s"
        type: ISSUE
        first: 100
        after: %s
      ) {
        nodes {
          ... on PullRequest {
            repository {
              nameWithOwner
            }
            id
            createdAt
            author {
              login
            }
            mergedAt
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
      }
    }
                """ % (repository, since_date, after_cursor)
            )
            response = client.execute(query)

            changes = response['search']['nodes']
            should_fetch_next_batch = response['search']['pageInfo']['hasNextPage']
            after_cursor = '"' + response['search']['pageInfo']['endCursor'] + '"'

            result.extend(changes)
        return result