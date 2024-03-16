# Examples

## [tastyware/tastytrade](https://github.com/tastyware/tastytrade)

Developing a personal project using this python library was the motivation behind this project.

### User Prompts (Questions)

1. How do I connect to a sandbox instance of the tastytrade api?
2. How do I view the net liquidity history of an account?
3. Generate a python script to get the net liquidity history of an account in the sandbox environment.

### Results

[Raw Output](https://www.notion.so/Chat-with-Files-e75a640625304606943dc02dd9cf51ee?pvs=21)

**Question**: How do I connect to a sandbox instance of the tastytrade api?

**Answer**: To connect to a sandbox (certification) instance of the Tastytrade API, you need to:

1. Create a certification account on the Tastytrade developer site: [https://developer.tastytrade.com/sandbox/](https://developer.tastytrade.com/sandbox/)
2. Use the `CertificationSession` class from the tastytrade Python SDK to create a session with your certification account credentials:

```python
from tastytrade import CertificationSession

session = CertificationSession('your_cert_username', 'your_cert_password')

```

The `CertificationSession` works the same way as the `ProductionSession`, but connects to Tastytrade's certification environment instead of the live production environment.

Note that certification accounts have some limitations compared to real production accounts, such as:

- Limited buying power
- Unable to place multi-leg orders
- Unable to modify or cancel orders
- Market data delays

But they allow you to test out the API integration and basic order flow safely before moving to a production account.

The documentation provides some examples of using the `CertificationSession`: [https://tastyworks-api.readthedocs.io/en/latest/sessions.html#certification-session](https://tastyworks-api.readthedocs.io/en/latest/sessions.html#certification-session)

**Question**: How do I view the net liquidity history of an account?

**Answer**: To view the net liquidity history of an account using the Tastytrade API, you can use the `get_net_liquidating_value_history` method of the `Account` class. Here's an example:

```python
from tastytrade import Account

account = Account.get_accounts(session)[0] # Get the first account
nl = account.get_net_liquidating_value_history(session, time_back='1m') # Past 1 month

# nl will contain a list of NetLiqOhlc objects representing the net liquidating value history
for snapshot in nl:
    print(f"Time: {snapshot.time}, Close: {snapshot.close}")

```

The `get_net_liquidating_value_history` method takes two optional parameters:

- `time_back` (str): The time period to get net liquidating value snapshots for. Possible values are '1d', '1m', '3m', '6m', '1y', 'all'.
- `start_time` (datetime): The start point for the query. If provided, this will take precedence over `time_back`.

It returns a list of `NetLiqOhlc` objects, each containing details like the timestamp, open, high, low and close net liquidating values for that snapshot.

So in the example, we're fetching the net liquidating value history for the past 1 month and printing the timestamp and close value for each snapshot.

**Question**: Generate a python script to get the net liquidity history of an account in the sandbox environment.

**Answer**: To get the net liquidity history of an account in the Tastytrade sandbox (certification) environment using Python, you can use the `get_net_liquidating_value_history` method from the `Account` class. Here's an example script:

```python
from tastytrade import CertificationSession, Account
from datetime import datetime, timedelta

# Create a certification session
session = CertificationSession(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD"
)

# Get the first account
account = Account.get_accounts(session)[0]

# Get net liquidity history for the past month
end_time = datetime.now()
start_time = end_time - timedelta(days=30)

net_liq_history = account.get_net_liquidating_value_history(
    session,
    start_time=start_time
)

# Print the net liquidity values
for snapshot in net_liq_history:
    print(f"Time: {snapshot.time}, Net Liquidity: {snapshot.close}")

```

Make sure to replace `"YOUR_USERNAME"` and `"YOUR_PASSWORD"` with your actual Tastytrade certification credentials.

This script will:

1. Create a `CertificationSession` with your credentials.
2. Get the first account associated with the session.
3. Fetch the net liquidity history for the past 30 days using `get_net_liquidating_value_history`.
4. Print out each net liquidity snapshot with its timestamp.

Note that the `get_net_liquidating_value_history` method accepts either a `time_back` parameter (e.g. `'1m'`, `'3m'`, `'1y'`) or a `start_time` parameter. In the example, we use `start_time` to specify the start date for the history.

### Debug/Run

Answer 3 looked the best to get started with.  I ended up with this after debugging:

*Note: The certification environment was having outages, so I used a ProductionSession.*

```python
from tastytrade import CertificationSession, Account

# Create a Certification session
session = CertificationSession(
    login="username",
    password="password"
)

# Get the first account
account = Account.get_accounts(session)[0]

# Get net liquidity history for the past month
net_liq_history = account.get_net_liquidating_value_history(
    session,
    time_back='1m'
)

# Print the net liquidity values
for snapshot in net_liq_history:
    print(f"Time: {snapshot.time}, Net Liquidity: {snapshot.close}")
```

![Screenshot 2024-03-16 at 3.09.30 PM.png](Chat%20with%20Files%20e75a640625304606943dc02dd9cf51ee/Screenshot_2024-03-16_at_3.09.30_PM.png)

### **Raw Output**

```
**Question**: How do I connect to a sandbox instance of the tastytrade api? 

**Answer**: To connect to a sandbox (certification) instance of the Tastytrade API, you need to:

1. Create a certification account on the Tastytrade developer site: https://developer.tastytrade.com/sandbox/

2. Use the `CertificationSession` class from the tastytrade Python SDK to create a session with your certification account credentials:

```python
from tastytrade import CertificationSession

session = CertificationSession('your_cert_username', 'your_cert_password')
```

The `CertificationSession` works the same way as the `ProductionSession`, but connects to Tastytrade's certification environment instead of the live production environment.

Note that certification accounts have some limitations compared to real production accounts, such as:

- Limited buying power
- Unable to place multi-leg orders
- Unable to modify or cancel orders
- Market data delays

But they allow you to test out the API integration and basic order flow safely before moving to a production account.

The documentation provides some examples of using the `CertificationSession`: https://tastyworks-api.readthedocs.io/en/latest/sessions.html#certification-session 

**Question**: How do I view the net liquidity history of an account? 

**Answer**: To view the net liquidity history of an account using the Tastytrade API, you can use the `get_net_liquidating_value_history` method of the `Account` class. Here's an example:

```python
from tastytrade import Account

account = Account.get_accounts(session)[0] # Get the first account
nl = account.get_net_liquidating_value_history(session, time_back='1m') # Past 1 month

# nl will contain a list of NetLiqOhlc objects representing the net liquidating value history
for snapshot in nl:
    print(f"Time: {snapshot.time}, Close: {snapshot.close}")
```

The `get_net_liquidating_value_history` method takes two optional parameters:

- `time_back` (str): The time period to get net liquidating value snapshots for. Possible values are '1d', '1m', '3m', '6m', '1y', 'all'.
- `start_time` (datetime): The start point for the query. If provided, this will take precedence over `time_back`.

It returns a list of `NetLiqOhlc` objects, each containing details like the timestamp, open, high, low and close net liquidating values for that snapshot.

So in the example, we're fetching the net liquidating value history for the past 1 month and printing the timestamp and close value for each snapshot. 

**Question**: Generate a python script to get the net liquidity history of an account in the sandbox environment. 

**Answer**: To get the net liquidity history of an account in the Tastytrade sandbox (certification) environment using Python, you can use the `get_net_liquidating_value_history` method from the `Account` class. Here's an example script:

```python
from tastytrade import CertificationSession, Account
from datetime import datetime, timedelta

# Create a certification session
session = CertificationSession(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD"
)

# Get the first account
account = Account.get_accounts(session)[0]

# Get net liquidity history for the past month
end_time = datetime.now()
start_time = end_time - timedelta(days=30)

net_liq_history = account.get_net_liquidating_value_history(
    session,
    start_time=start_time
)

# Print the net liquidity values
for snapshot in net_liq_history:
    print(f"Time: {snapshot.time}, Net Liquidity: {snapshot.close}")
```

Make sure to replace `"YOUR_USERNAME"` and `"YOUR_PASSWORD"` with your actual Tastytrade certification credentials.

This script will:

1. Create a `CertificationSession` with your credentials.
2. Get the first account associated with the session.
3. Fetch the net liquidity history for the past 30 days using `get_net_liquidating_value_history`.
4. Print out each net liquidity snapshot with its timestamp.

Note that the `get_net_liquidating_value_history` method accepts either a `time_back` parameter (e.g. `'1m'`, `'3m'`, `'1y'`) or a `start_time` parameter. In the example, we use `start_time` to specify the start date for the history. 

```
