import os
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv

# Load server environment parameters
load_dotenv()

try:
    # Establish a singular shared database connection
    connection = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE")
    )

    if connection.is_connected():
        print("Connected to MySQL. Generating multiple corporate reports...")

        # ====================================================================
        # REPORT 1: EQUIPMENT PURCHASES VS RENTALS
        # ====================================================================
        query1 = """
        SELECT
            p.transaction_type AS `Transaction Type`,
            COUNT(p.purchase_id) AS `Total Transactions`
        FROM equipment_purchase p
        GROUP BY p.transaction_type
        ORDER BY `Total Transactions` DESC;
        """
        df1 = pd.read_sql(query1, connection)
        report1_filename = "report1_sales_vs_rentals.csv"
        with open(report1_filename, mode="w", newline="", encoding="utf-8") as file:
            file.write("========================================================\n")
            file.write("        OUTLAND ADVENTURES - BUSINESS PERFORMANCE       \n")
            file.write("========================================================\n")
            file.write("Author Team  : Green Team\n")
            file.write("Question     : Do enough customers buy equipment to keep equipment sales?\n")
            file.write(f"Run Date     : {datetime.now().strftime('%B %d, %Y')}\n")
            file.write("--------------------------------------------------------\n\n")
            df1.to_csv(file, index=False)

        plt.figure(figsize=(6, 4))
        bars1 = plt.bar(df1['Transaction Type'], df1['Total Transactions'], color=['#34495E', '#1ABC9C'], edgecolor='black', width=0.4)
        for bar in bars1:
            plt.annotate(f'{int(bar.get_height())}', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontweight='bold')
        plt.title("Equipment Transactions: Buy vs. Rent", fontsize=11, fontweight='bold')
        plt.ylabel("Orders Count")
        plt.savefig("report1_sales_vs_rentals_chart.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Report 1 Completed.")

        # ====================================================================
        # REPORT 2: TRIP BOOKING TRENDS BY LOCATION
        # Business Question: Is there any location that has a downward trend in bookings?
        # ====================================================================
        query2 = """
        SELECT
            t.location AS `Trip Location`,
            COUNT(b.booking_id) AS `Total Bookings`
        FROM trip t
        LEFT JOIN booking b ON t.trip_id = b.trip_id
        GROUP BY t.location
        ORDER BY `Total Bookings` ASC;
        """
        df2 = pd.read_sql(query2, connection)
        report2_filename = "report2_trip_booking_trends.csv"
        with open(report2_filename, mode="w", newline="", encoding="utf-8") as file:
            file.write("========================================================\n")
            file.write("         OUTLAND ADVENTURES - BOOKING ANALYSIS          \n")
            file.write("========================================================\n")
            file.write("Author Team  : Green Team\n")
            file.write("Question     : Is there any location that has a downward trend in bookings?\n")
            file.write(f"Run Date     : {datetime.now().strftime('%B %d, %Y')}\n")
            file.write("--------------------------------------------------------\n\n")
            df2.to_csv(file, index=False)

        plt.figure(figsize=(8, 4))
        bars2 = plt.bar(df2['Trip Location'], df2['Total Bookings'], color='#2980B9', edgecolor='black', width=0.5)
        for bar in bars2:
            plt.annotate(f'{int(bar.get_height())}', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontweight='bold')
        plt.title("Trip Bookings Volume by Destination Location", fontsize=11, fontweight='bold')
        plt.ylabel("Number of Bookings")
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.savefig("report2_trip_booking_trends_chart.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Report 2 Completed.")

          # ====================================================================
        # REPORT 3: EQUIPMENT OLDER THAN 5 YEARS (REVISED BY AGE COLUMN)
        # Business Question: Are there inventory items that are over five years old?
        # ====================================================================
        # REVISION: Selects directly from the pre-calculated equipment_age column
        query3 = """
        SELECT
            equipment_name AS `Equipment Item`,
            equipment_age AS `Stored Age (Years)`,
            condition_status AS `Condition`,
            needs_inspection AS `Needs Inspection`,
            status AS `Availability Status`
        FROM equipment
        WHERE equipment_age > 5
        ORDER BY `Stored Age (Years)` DESC;
        """
        df3 = pd.read_sql(query3, connection)
        report3_filename = "report3_aged_inventory.csv"

        with open(report3_filename, mode="w", newline="", encoding="utf-8") as file:
            file.write("========================================================\n")
            file.write("         OUTLAND ADVENTURES - INVENTORY AUDIT           \n")
            file.write("========================================================\n")
            file.write("Author Team  : Green Team\n")
            file.write("Question     : Are there inventory items that are over five years old? (By Age Column)\n")
            file.write(f"Run Date     : {datetime.now().strftime('%B %d, %Y')}\n")
            file.write("--------------------------------------------------------\n\n")
            df3.to_csv(file, index=False)

        # Generate Graph 3 matching your exact data bounds
        plt.figure(figsize=(8, 4))
        if not df3.empty:
            bars3 = plt.bar(df3['Equipment Item'], df3['Stored Age (Years)'], color='#D35400', edgecolor='black', width=0.4)
            for bar in bars3:
                plt.annotate(f'{int(bar.get_height())} yrs', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                            xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

        plt.title("Aged Inventory Metrics (Items > 5 Years Old from Schema)", fontsize=11, fontweight='bold')
        plt.xlabel("Equipment Item")
        plt.ylabel("Asset Age (Years)")
        plt.grid(axis='y', linestyle='--', alpha=0.5)

        graph3_filename = "report3_aged_inventory_chart.png"
        plt.savefig(graph3_filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Report 3 Revised Successfully.")

except mysql.connector.Error as error:
    print(f"Error connecting to MySQL: {error}")

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("\nAll tasks finalized. Database connection closed cleanly.")