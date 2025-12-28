@double11_promotion
Feature: Double 11 Sale Promotions
  As a shopper
  I want the system to apply Double 11 bulk discount promotions to my order
  So that I can understand how much to pay and what items I will receive

  Background:
    Given the Double 11 promotion is active
    And the bulk discount rule for Double 11 is:
      | groupSize | discountRate |
      | 10        | 20%          |

  Scenario: Purchase 12 units of same product - discount applies to first 10 units only
    When a customer places an order with:
      | productName | quantity | unitPrice |
      | Socks       | 12       | 100       |
    Then the order summary should be:
      | originalAmount | discount | totalAmount |
      | 1200           | 200      | 1000        |
    And the customer should receive:
      | productName | quantity |
      | Socks       | 12       |

  Scenario: Purchase 27 units of same product - discount applies to two sets of 10 units
    When a customer places an order with:
      | productName | quantity | unitPrice |
      | Socks       | 27       | 100       |
    Then the order summary should be:
      | originalAmount | discount | totalAmount |
      | 2700           | 400      | 2300        |
    And the customer should receive:
      | productName | quantity |
      | Socks       | 27       |

  Scenario: Purchase 10 different products - no discount applied
    When a customer places an order with:
      | productName | quantity | unitPrice |
      | Product-A   | 1        | 100       |
      | Product-B   | 1        | 100       |
      | Product-C   | 1        | 100       |
      | Product-D   | 1        | 100       |
      | Product-E   | 1        | 100       |
      | Product-F   | 1        | 100       |
      | Product-G   | 1        | 100       |
      | Product-H   | 1        | 100       |
      | Product-I   | 1        | 100       |
      | Product-J   | 1        | 100       |
    Then the order summary should be:
      | originalAmount | discount | totalAmount |
      | 1000           | 0        | 1000        |
    And the customer should receive:
      | productName | quantity |
      | Product-A   | 1        |
      | Product-B   | 1        |
      | Product-C   | 1        |
      | Product-D   | 1        |
      | Product-E   | 1        |
      | Product-F   | 1        |
      | Product-G   | 1        |
      | Product-H   | 1        |
      | Product-I   | 1        |
      | Product-J   | 1        |