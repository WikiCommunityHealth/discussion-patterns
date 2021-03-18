# Documentation Talkpage Metrics

### Table structure

Each record in the table has the following structure:
- `id`
- `page_id`: unique identifier of the talk page
- `metric_name`
- `year_month` with format YYYY/MM
- `absolute_actual_value`: metric value for the current month
- `absolute_cumulative_value`: sum up of the metric values until year_month
- `relative_actual_value`: absolute_actual_value / sum up of all the metric values for the current talk page
- `relative_cumulative_value`: absolute_cumulative_value / sum up of all the metric values for the current talk page

### List of metrics implemented
- number of users in the discussion
- number of total actions
- number of additions
- number of creations
- number of modifications
- number of deletions
- number of restorations
- max depth of the conversation
- number of toxic messages
- number of severe toxic messages
- number of revision comment with "vandalism" keyword

### List of metrics not implemented
- number of actions by bots
- number of revisions
- number of mutual chains with length >=3
- number of mutual chains with length >=5
- number of mutual chains with length >=7
- number of mutual chains with length >=9
- h-index: maximum number h s.t. there are >= h messages with depth >= h
- delta-h-index
- u-index: maximum number u s.t. there are >= u users with >= u messages
- delta max depth: difference between the last month and the current one
- commenti all'interno di una catena mutua