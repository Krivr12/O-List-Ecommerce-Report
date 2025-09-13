# Business and Operation Analysis for Brazilian E-Commerce 
## Executive Summary:

Using Python and AWS, I pulled the data from the cloud storage and created a dashboard to easily track our progress. I identified that the largest bottleneck in our operation is "Carrier -> Customer" Stage and that customer retention rate is low, with 3.9% being the highest. With that, the largest revenue opportunities are to increase and identify strategic warehouse location and to create actions like loyalty discounts and repeat order promos. I recommend that the logistic and marketing team create a joint operation they will review the process and suggest changes that would lead to:

1. Faster delivery rate, especially on low performing regions like Bahia (BA).
2. Higher customer retention rate.
3. Maintain the momentum and further grow demand in emerging states like Parana (PR).
4. Drastic increase in revenue.

---
## Business Problem:

Fast and on-time orders are essential for an e-commerce platform like Olist, this affect customer satisfaction and retention rate. I noticed that there's a severe delayed delivery in order states, with some reaching up to 26 days, almost doubled the average delivery times of 12 days, and aside from that it is also visible that we still have a low retention rate. The goal is how can we identify on which stage in the operation is the root cause of this delayed, and on which states should we focus our resources more for greater ROI.

<img width="1062" height="568" alt="image" src="https://github.com/user-attachments/assets/39aef07c-c542-4b65-b5b4-24d291fe223d" />

You can see that we have greater number of orders with states that have short delivery time compared to states. 

## Methodology:

1. Use Boto3 to create a connection with AWS and perform data retrieval to have accessed with the raw files.
2. Conduct ETL using python to prepare data for analyzation.
3. Performed statistical analysis on both the Business Performance and Operation.
4. Created a dashboard using streamlit for better visualization and tracking of status and performance of the platform.
5. Provide actionable insights that would have great impact within the business.

## Skills:
1. AWS: S3 for storing raw and processed data, Athena to have initial query on the data
2. Python: Pandas to manipulate data, Numpy for computation,
   
## Results and Business Recommendation:
On average, monthly orders grew by 306 orders, showing steady growth due to some ups and down which might be caused of different shopping pattern depending on the season. Despite this consistent growth, we have declining states like Tocantins (TO) and Espirito Santo (ES) with an 8% decline from the number of orders from the start and end of the period. 
<img width="898" height="494" alt="image" src="https://github.com/user-attachments/assets/5c7784d7-9bd5-42b1-8665-cae4bcbdf89e" />

I also discovered the Sao Paolo (SP) is the main contributor with 41,621 orders (42%) followed by Rio de Janeiro (RJ)  with 12,792 (13%). This create a high dependency in Sao Paulo. Having a huge and consistent market would allow us to balance our growth, I suggest that we should diversify our resources into emerging states like Paraná and Rio Grande do Sul with each sharing 5% market share. But we should also create actions that would support and address declining markets.
<img width="724" height="408" alt="image" src="https://github.com/user-attachments/assets/f8c73cdd-800f-4a66-b24c-a4595577f840" />

Carrier -> Customer stage also proves to be the orimary bottleneck that cause delays on most of the order with a 100% result of each month, accounting to 9.3 days or 77% of the average total process time. This is followed by the approval process due to its considerable variability that could further increase this delay. This can be solve by reviewing the overall operational process and having an intensive geographic market study that would help us find a suitable location for an additional warehouse that would have the highest impact while keeping the cost low.
<img width="678" height="395" alt="image" src="https://github.com/user-attachments/assets/dc74e89d-d73d-4d61-9aba-de8857662e76" />

For in-depth analysis, check these notebooks: [Business Performance Analysis](https://github.com/Krivr12/O-List-Ecommerce-Report/blob/master/notebook/Business_Performance.ipynb) and [Operation Analysis](https://github.com/Krivr12/O-List-Ecommerce-Report/blob/master/notebook/Operational_Analysis.ipynb) 


## Next Steps:
1. Access location and delivery routes to provide a more efficient process.
2. Adjust operation stages within our scope mainly the Approval -> Carrier Stage.
3. Cooperate with marketing team to plan the best way to balance our current market status.


## Developer  

**Chris Evangelista**  
Polytechnic University of the Philippines | AWS Cloud Clubs PUP  

[LinkedIn](https://www.linkedin.com/in/chrisbryevangelista12/)
