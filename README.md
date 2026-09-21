\# 💳 Payment Gateway Simulator



A Flask-based payment gateway simulator that demonstrates payment orchestration across multiple Payment Service Providers (PSPs), round-robin routing, health checks, automatic failover, and transaction logging.



\## 📌 Project Overview



The Payment Gateway Simulator acts as an intermediate layer between a customer and multiple simulated Payment Service Providers.



Instead of sending every payment request to a single PSP, the gateway:



\- Routes payments across multiple PSPs

\- Performs PSP health checks

\- Detects unavailable PSPs

\- Automatically switches to another PSP when a PSP fails

\- Generates unique transaction IDs

\- Records payment transactions and processing time



This project demonstrates concepts used in distributed payment processing systems.



\---



\## 🏗️ Architecture



```text

\&#x20;                Customer

\&#x20;                   |

\&#x20;                   v

\&#x20;         +--------------------+

\&#x20;         |  Payment Gateway   |

\&#x20;         |      Flask         |

\&#x20;         |      :5000         |

\&#x20;         +--------------------+

\&#x20;                   |

\&#x20;            PSP Health Check

\&#x20;                   |

\&#x20;       +-----------+-----------+

\&#x20;       |           |           |

\&#x20;       v           v           v

\&#x20;    +------+    +------+    +------+

\&#x20;    | PSP1 |    | PSP2 |    | PSP3 |

\&#x20;    | :5001|    | :5002|    | :5003|

\&#x20;    +------+    +------+    +------+

\&#x20;       |           |           |

\&#x20;       +-----------+-----------+

\&#x20;                   |

\&#x20;                   v

\&#x20;           Payment Response

\&#x20;                   |

\&#x20;                   v

\&#x20;         Transaction Logging

\&#x20;                   |

\&#x20;                   v

\&#x20;         transactions.csv


