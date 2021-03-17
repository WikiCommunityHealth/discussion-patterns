# Documentation Talkpage Matrics

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




### List of metrics not implemented
- number of actions by bots

- number of revisions
- number of mutual chains with length >=3
- number of mutual chains with length >=5
- number of mutual chains with length >=7
- number of mutual chains with length >=9
- number of toxic messages
- number of super toxic messages
- h-index: h messages with at least depth h
- u-index: u users with at least u messages
- numeber of messages at a current indentation by month