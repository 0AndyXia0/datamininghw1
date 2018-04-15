# coding = utf-8
import pandas
from pandas import Series
import matplotlib
from matplotlib import pyplot
from matplotlib.font_manager import FontProperties
import numpy
import time
import json
import math

import scipy.stats as stats
DataFile = open("F:/Users/andy/Documents/HW/Building_Permits.csv",encoding='gb18030',errors='ignore')
#DataFile = open("F:/Users/andy/Documents/HW/NFL Play by Play 2009-2017 (v4).csv",encoding='gb18030',errors='ignore')
DataTable = pandas.read_csv(DataFile);
DataTable = DataTable.dropna(axis=1, how='all');
# 标称属性
#'''
NominalAttribute = ['Permit Number', 'Permit Type', 'Permit Type Definition', 'Permit Creation Date', 'Block', 'Lot',
                    'Street Number', 'Street Number Suffix', 'Street Name', 'Street Name Suffix', 'Unit suffix',
                    'Description', 'Current Status', 'Current Status Date', 'Filed Date', 'Issued Date',
                    'Completed Date', 'First Construction Document Date', 'Structural Notification', 'Fire Only Permit',
                    'Permit Expiration Date', 'Existing Use', 'Proposed Use', 'Plansets', 'TIDF Compliance',
                    'Existing Construction Type', 'Existing Construction Type Description',
                    'Proposed Construction Type', 'Proposed Construction Type DescriptionSite Permit',
                    'Neighborhoods - Analysis Boundaries', 'Zipcode', 'Location'];
NumericAttribute = ['Unit', 'Number of Existing Stories', 'Number of Proposed Stories', 'Estimated Cost',
                   'Revised Cost', 'Existing Units', 'Proposed Units', 'Supervisor District'];
'''
NominalAttribute = ['Date', 'GameID', 'time', 'SideofField', 'FirstDown', 'posteam', 'DefensiveTeam', 'desc',
                    'PlayAttempted', 'Yards.Gained', 'sp', 'Touchdown', 'ExPointResult', 'TwoPointConv', 'DefTwoPoint',
                    'Onsidekick', 'Safety', 'PuntResult', 'PlayType', 'Passer', 'Passer_ID', 'PassAttempt',
                    'PassOutcome', 'PassLength', 'QBHit', 'PassLocation', 'InterceptionThrown', 'Interceptor', 'Rusher',
                    'Rusher_ID', 'RushAttempt', 'RunLocation', 'RunGap', 'Receiver', 'Receiver_ID', 'Reception',
                    'ReturnResult', 'Returner', 'BlockingPlayer', 'Tackler1', 'Tackler2', 'FieldGoalResult', 'Fumble',
                    'RecFumbTeam', 'RecFumbPlayer', 'Sack', 'Challenge.Replay', 'ChalReplayResult', 'Accepted.Penalty',
                    'PenalizedTeam', 'PenaltyType', 'PenalizedPlayer', 'HomeTeam', 'AwayTeam', 'Timeout_Indicator',
                    'Timeout_Team', 'Season', 'posteam_timeouts_pre', 'HomeTimeouts_Remaining_Pre',
                    'AwayTimeouts_Remaining_Pre', 'HomeTimeouts_Remaining_Post', 'AwayTimeouts_Remaining_Post'];
NumericAttribute = ['Drive', 'qtr', 'down', 'TimeUnder', 'TimeSecs', 'PlayTimeDiff', 'yrdln', 'yrdline100', 'ydstogo',
                    'ydsnet', 'GoalToGo', 'AirYards', 'YardsAfterCatch', 'FieldGoalDistance', 'Penalty.Yards',
                    'PosTeamScore', 'DefTeamScore', 'ScoreDiff', 'AbsScoreDiff', 'No_Score_Prob', 'Opp_Field_Goal_Prob',
                    'Opp_Safety_Prob', 'Opp_Touchdown_Prob', 'Field_Goal_Prob', 'Safety_Prob', 'Touchdown_Prob',
                    'ExPoint_Prob', 'TwoPoint_Prob', 'ExpPts', 'EPA', 'airEPA', 'yacEPA', 'Home_WP_pre', 'Away_WP_pre',
                    'Home_WP_post', 'Away_WP_post', 'Win_Prob', 'WPA', 'airWPA', 'yacWPA'];
BinaryAttribute = ['GoalToGo', 'FirstDown', 'sp', 'Touchdown', 'ExPointResult', 'Onsidekick', 'PuntResult',
                   'PassAttempt', 'PassOutcome', 'PassLength', 'QBHit', 'InterceptionThrown', 'RushAttempt'];
 '''
NominalAttributeAbstract = dict();
NumericAttributeAbstract = dict();

# 统计数据摘要
for i in DataTable.columns: 
    if i in NominalAttribute: 
        DataColumn = DataTable[i];  
        DataColumnStatistic = DataColumn.value_counts();
        tmpDict = DataColumnStatistic.to_dict(); 
        NominalAttributeAbstract[i] = tmpDict;
    elif i in NumericAttribute:  
        DataColumn = DataTable[i];  
        tmpList = [DataColumn.max(), DataColumn.min(), DataColumn.mean(), DataColumn.median(),
                   DataColumn.quantile(0.25), DataColumn.quantile(0.75), DataColumn.isnull().sum()];
        NumericAttributeAbstract[i] = tmpList;
        
    else:
        continue;
else:
    print('数据摘要统计完成');
#输出到文件
    jsObj = json.dumps(NominalAttributeAbstract)  
    fileObject = open('jsonFile.json', 'w')  
    fileObject.write(jsObj)  
    fileObject.close()
    fw=open('result.txt','w'); 
    fw.write(str(NumericAttributeAbstract));    
    fw.close();
for i in DataTable.columns:
    if i in NumericAttribute:
        DataColumn = DataTable[i]; 
        #MostFrequentElement = DataColumn.value_counts().idxmax();
        #DataColumn = DataColumn.fillna(value=MostFrequentElement);  # 众数填补缺失值
        DataColumn = DataColumn.dropna(axis=0, how='any');#删除
        pyplot.hist(DataColumn,bins=50, normed=1);
        pyplot.title(i)
        pyplot.savefig(i+"_histogram.png")
       # pyplot.show()
        pyplot.close()
else:
    print('直方图绘制完成');

for i in DataTable.columns:
    if i in NumericAttribute:
        DataColumn = DataTable[i];  # 获取该列
        #MostFrequentElement = DataColumn.value_counts().idxmax();
        #DataColumn = DataColumn.fillna(value=MostFrequentElement);  # 众数填补缺失值
        DataColumn = DataColumn.dropna(axis=0, how='any');#删除
        fig=pyplot.figure(1,figsize=(9,6))
        axes = fig.add_subplot(111)
        boxplot=axes.boxplot(DataColumn)
        fig.savefig(i+"_box-plot.png",bbox_inches='tight')
        pyplot.title(i)
      #  pyplot.show()
        pyplot.close()
else:
    print('盒图绘制完成');

for i in DataTable.columns:
    if i in NumericAttribute:
        DataColumn = DataTable[i];  # 获取该列
        #MostFrequentElement = DataColumn.value_counts().idxmax();
        #DataColumn = DataColumn.fillna(value=MostFrequentElement);  # 众数填补缺失值
        DataColumn = DataColumn.dropna(axis=0, how='any');#删除
        stats.probplot(DataColumn,dist="norm",plot=pyplot)
        pyplot.savefig(i+"_qq-plot.png")
        pyplot.title(i)
        #pyplot.show()
        pyplot.close()
else:
    print('QQ图绘制完成');
