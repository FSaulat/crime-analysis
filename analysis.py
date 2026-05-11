import threading
import time
import pandas as pd
import matplotlib.pyplot as plt

class crimeAnalysis:

    def spinner(self, stop_flag):
        chars = ['/', '-', '\\', '|']
        i = 0
        while not stop_flag[0]:
            print(f'\rLoading CSV {chars[i]}', end='', flush=True)
            i = (i + 1) % 4
            time.sleep(0.1)

    def load_data(self, filepath):
        stop_flag = [False]
        t = threading.Thread(target=self.spinner, args=(stop_flag,))
        t.start()
        
        df = pd.read_csv(filepath)
        
        stop_flag[0] = True
        return df

    def scanning(self, df):
    #  Finding top crime

    # BIASES & LIMITATIONS OF THIS ANALYSIS:
    # --------------------------------
    # 1. Reporting bias: Only includes reported crimes (dark figure of crime)
    # 2. Frequency ≠ severity: Most common crime may not be most harmful
    # 3. Detection bias: High-patrol areas show artificially higher crime counts
    # 4. Single-crime focus: Only analyzing TOP crime, not #2 or #3
    # 5. Data quality: Relies on accurate police recording and classification
    # --------------------------------

        crime_counts = df['Crm Cd Desc'].value_counts()
        top_crime = crime_counts.index[0]
        top_count = crime_counts.iloc[0]

        print(f" Top Crime: {top_crime}")
        print(f"Count: {top_count} out of {len(df):,} total crimes")
        print(f"Percentage: {top_count/len(df)*100:.1f} %")
        
        return top_crime
    
    # --------------------------------
    # --------------------------------
    # CRIME TRIANGLE 
    # --------------------------------
    # --------------------------------

    # --------------------------------
    # Location analysis
    # --------------------------------
    def location(self, df, top_crime):
        # identifies geographic hotspots for target (top) crime

        crime_df = df[df['Crm Cd Desc'] == top_crime] # filters analysis for only the top crime

        area_counts = crime_df['AREA NAME'].value_counts() # counts crimes by area

        top_hotspot = area_counts.index[0]
        hotspot_count = area_counts.iloc[0]
        percentage = hotspot_count / len(crime_df) * 100

        print(f"Hotspot for : {top_crime} : {top_hotspot}")
        print(f"Number of incidents: {hotspot_count}")
        print(f"Percentage: {percentage:.1f}%")

        return top_hotspot

    
    # --------------------------------
    # Victim analysis
    # --------------------------------
    def victim(self, df, top_crime):
        #  Analyzes WHO is being targeted

        crime_df = df[df['Crm Cd Desc'] == top_crime] # filters analysis for only the top crime

        print(f"\n{'='*50}")
        print("Victim/Target")
        print('='*50)
        print(f"\nAnalyzing victims of: {top_crime}")


        print(f"\n VICTIM AGE:")
        if "Vict Age" in crime_df.columns:
            ages = crime_df['Vict Age'].dropna()
            ages = ages[(ages > 0) & (ages < 100)] 
            if len(ages) > 0:
                avg_age = ages.mean()
                top_age = ages.mode()[0]

                print(f"   Average age: {avg_age:.1f} years")
                print(f"   Most common age: {top_age:.0f} years")
                print(f"   Age range: {ages.min():.0f} - {ages.max():.0f}")

                valid_pct = (len(ages) / len(crime_df)) * 100
                print(f"   (Age available for {valid_pct:.1f}% of cases)")
            else:
                print(f"   No valid age data available")

        print(f"\n VICTIM Gender:")
        if "Vict Sex" in crime_df.columns:
            gender_counts = crime_df['Vict Sex'].value_counts()
            top_gender = gender_counts.index[0]
            top_gender_count = gender_counts.iloc[0]
            gender_percentage = (top_gender_count / len(crime_df)) * 100

            print(f"   Most common gender: {top_gender}")
            print(f"   Count: {top_gender_count:,} ({gender_percentage:.1f}%)")

        print(f"\n VICTIM Ethnicity/Descent:")
        if "Vict Descent" in crime_df.columns:
            descent_counts = crime_df['Vict Descent'].value_counts()

            top_descent = descent_counts.index[0]
            top_descent_count = descent_counts.iloc[0]
            descent_percentage =  top_descent_count/ len(crime_df) * 100
           
            print(f"   Most common descent: {top_descent}")
            print(f"   Count: {top_descent_count:,} ({descent_percentage:.1f}%)")
    
    # --------------------------------
    # Offender analysis
    # --------------------------------
    def offender(self, df, top_crime):
        # when and how they are striking

        crime_df = df[df['Crm Cd Desc'] == top_crime] # filters analysis for only the top crime
        
        print(f"\n{'='*50}")
        print("Offender")
        print('='*50)
        print(f"\nAnalyzing offenders of : {top_crime}")

        # Time Analysis

        print(f"Time Pattern: ")
        if "TIME OCC" in crime_df.columns:
            crime_df['HOUR'] = crime_df['TIME OCC'] // 100
            peak_hour = crime_df['HOUR'].mode()[0]
            print(f"   Peak crime hour: {peak_hour}:00")

            night = crime_df['HOUR'].between(20, 24) | crime_df['HOUR'].between(0, 4)
            night_percentage = (night.sum() / len(crime_df)) * 100
            print(f"   Nighttime crimes (8pm-4am): {night_percentage:.1f}%")

        print(f"Day of the Week: ")
        if "DATE OCC" in crime_df.columns:
            crime_df['DOW'] = pd.to_datetime(crime_df["DATE OCC"]).dt.dayofweek
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            peak_day = crime_df['DOW'].mode()[0]
            peak_day_name = days[peak_day]
            print(f"   Peak crime day: {peak_day_name}")

            weekend = crime_df['DOW'].isin([5, 6])
            weekend_percentage = (weekend.sum() / len(crime_df)) * 100
            print(f"   Weekend crimes (Sat-Sun): {weekend_percentage:.1f}%")

        print (f"Location Type")
        if "Premis Desc" in crime_df.columns:
            premis_counts = crime_df['Premis Desc'].value_counts()
            top_premis = premis_counts.index[0]
            top_premis_count = premis_counts.iloc[0]
            top_premis_percentage =  premis_counts.iloc[0] / len(crime_df) * 100
            print(f"    Most common: {top_premis}")
            print(f"    {top_premis_count:,} incidents ({top_premis_percentage:.1f})%")
            
        # Weapon Analysis
        print(f"\n Weapon Usage:")
        if "Weapon Desc" in crime_df.columns:
            weapon_counts = crime_df['Weapon Desc'].value_counts()

            top_weapon = weapon_counts.index[0]
            top_weapon_count = weapon_counts.iloc[0]
            weapon_percentage =  top_weapon_count/ len(crime_df) * 100

            print(f"    Most common: {top_weapon}")
            print(f"    {top_weapon_count:,} incidents ({weapon_percentage:.1f})%")

            no_weapon = crime_df['Weapon Desc'].isna().sum()
            no_weapon_percentage = no_weapon/ len(crime_df) * 100
            print(f"  No weapon  {no_weapon:,} incidents ({no_weapon_percentage:.1f}%)")

        return {
        'peak_hour': peak_hour,
        'night_percentage': night_percentage,
        'peak_day': peak_day_name,
        'weekend_percentage': weekend_percentage,
        'top_location_type': top_premis,
        'top_weapon': top_weapon,
        'top_weapon_count': top_weapon_count,
        'no_weapon_percentage': no_weapon_percentage
    }

    def response(self, top_crime, hotspot, offender_data):
        #Ethical recommendations
        
        print(f"\n{'='*50}")
        print("RESPONSE: Ethical Interventions")
        print('='*50)
        
        print(f"\nBased on analysis of {top_crime} in {hotspot}:")
        
        # ========== FOR VICTIMS (Protection) ==========
        print(f"\n FOR VICTIMS:")
        print(f"   1. Target hardening: Security cameras in {hotspot}")
        print(f"   2. Community awareness programs")
        print(f"   3. Victim support services")
        
        # ========== FOR OFFENDERS (Root Causes) ==========
        print(f"\n FOR OFFENDERS (Addressing root causes):")
        
        # Time-based insights
        if offender_data.get('night_percentage', 0) > 40:
            print(f"   1. Late-night youth programs (alternative to crime)")
            print(f"   2. Improved lighting (reduces opportunity, helps everyone)")
        
        # Location-based insights  
        if offender_data.get('top_location_type'):
            location = offender_data['top_location_type']
            print(f"   3. Focus resources on {location} areas")
        
        # Weapon insights
        if offender_data.get('no_weapon_percentage', 0) > 50:
            print(f"   4. Opportunity reduction (crimes of convenience)")
        
        # Universal recommendations
        print(f"\n COMMUNITY-BASED (Helps both):")
        print(f"   • Job training programs in {hotspot}")
        print(f"   • Mental health and substance abuse services")
        print(f"   • Youth mentorship and after-school programs")
        print(f"   • Environmental design (lighting, parks, cleanliness)")
        
        # Ethical rationale
        print(f"\n ETHICAL RATIONALE:")
        print(f"   • Punishment-only approach doesn't address root causes")
        print(f"   • Prevention benefits entire community")
        print(f"   • Addresses social determinants of crime")
        
        return "Response complete"

    def main(self):
        df = self.load_data('Crime_Data_from_2020_to_2024.csv')
        print(df.columns.tolist())
        print(f"Dataset shape: rows: {df.shape[0]}, columns: {df.shape[1]}")

        #Sara step 1
        top_crime = self.scanning(df)
       

        # Sara step 2
        hotspot = self.location(df, top_crime)
        self.victim(df, top_crime)
        offender_data = self.offender(df, top_crime)

        # Sara step 3
        self.response(top_crime, hotspot, offender_data)

       
        

if __name__ == "__main__":
    analysis = crimeAnalysis()
    analysis.main()

    print(analysis)