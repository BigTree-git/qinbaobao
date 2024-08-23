import os 
import sys
import  re
import cn2an
import datetime
import inspect

def timeConvert(rudeTime):
    if rudeTime==None:return "-"
    rudeTime=re.sub(r"半", "30",rudeTime)  
    nums=re.findall("\d+",rudeTime)  
    if len(nums)>2:
        nums=nums[0:2]
    elif len(nums)==1:
        nums.append("00")
    if len(nums[0])==1:nums[0]="0"+nums[0]
    if len(nums[1])==1:nums[1]="0"+nums[1]
    if len(rudeTime)==0 or rudeTime=="-":
        return "-"
    return ":".join(nums)
def mergeTime(from0,to0):
    if from0=="-":
        return "-"
    elif to0=="-":
        return from0
    else:
        "-".join([from0,to0])
        
def sumConvert(rudeSum):
    if rudeSum==None:return "-"
    rudeSum=re.sub(r"[^0-9]+", "",rudeSum)     
    return rudeSum
def unitConvert(rudeSum):
    if rudeSum==None:return "-"
    if re.search(r"[分钟]",rudeSum):
        return "分钟"
    elif re.search(r"[盎司]",rudeSum):
        return "盎司"
    else:
        return "-"      
def typeConvert(rudeType):
    if rudeType==None:return "-"
    if re.search(r"[粉]",rudeType):
        return "奶粉"
    elif re.search(r"[母乳]",rudeType):
        return "母乳"
    else:
        return "-"  
def correctAns(ans,speech):#将时间0-12时间更改为离当前时间最近且大于的0-24时间
    ans["时间"]="09:33"
    curTime=datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
    splits=curTime.split("  ")
    date=splits[0]
    curTime = re.findall(r"\d{2}:", splits[1])   
    hour=curTime[0][0:2]  
    minute=curTime[1][0:2]
    if ans["时间"]=="-":               
        curTime=":".join([minute,second])     
        ans["时间"]="/".join([date,curTime])
    elif int(ans["时间"][0:2])<=12:#对大于12点的情况认为是下午，不进行纠正 
        while True:
            if re.search(r"明天早上|明早",speech):break                         
        curTimeInt=int(hour)*60+int(minute)
        checkTimeInt=int(ans["时间"][0:2])*60+int(ans["时间"][-2:] )
        if(checkTimeInt<curTimeInt):ans["时间"]=str(int(ans["时间"][0:2])+12)+ans["时间"][2:]
        checkTimeInt=int(ans["时间"][0:2])*60+int(ans["时间"][-2:])
        if(checkTimeInt<curTimeInt):
            #ToDo
            pass
def getCurTime():#将时间0-12时间更改为离当前时间最近且大于的0-24时间
    curTime=datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
    splits=curTime.split("  ")
    date=splits[0]
    curTime = re.findall(r"\d{2}:", splits[1])   
    hour=curTime[0][0:2]  
    minute=curTime[1][0:2]
    return hour,minute
def calSleepTime(ans):
    beginTime=["开始时间","入睡时间"]
    endTime=["结束时间","起床时间"]
    for i in beginTime:
        if i in ans:
            beginTime0=i
            break
    for i in endTime:
        if i in ans:
            endTime0=i
            break        
    
    curTime=datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
    splits=curTime.split("  ")
    date=splits[0]
    curTime = re.findall(r"\d{2}:", splits[1])   
    hour=curTime[0][0:2]  
    minute=curTime[1][0:2]
    if ans[beginTime0]=="-" or ans[endTime0]=="-":
        return "-"
    fromTime=int(ans[beginTime0].split(":")[0])*60+int(ans[beginTime0].split(":")[1])
    toTime=int(ans[endTime0].split(":")[0])*60+int(ans[endTime0].split(":")[1])
    # assert(toTime>=fromTime)
    sleepTime=str(int((toTime-fromTime)//60))+":"+str(int((toTime-fromTime)%60))
    if len(sleepTime.split(":")[1])==1:
        sleepTime=sleepTime.split(":")[0]+":0"+sleepTime.split(":")[1]
    return sleepTime
#放宽范围  综合中午上午是5-15点 下午是12-7点  晚上是 17-5
def checkoutTimeAm(from1):
    if ((int(from1[0:2])<=12 and int(from1[0:2])>=5) or (int(from1[0:2])>12 and int(from1[0:2])%12>0 and int(from1[0:2])%12<=3)):
        return True
    return False
def checkoutTimePm(from1):
    if (int(from1[0:2])%12>0 and int(from1[0:2])%12<=7):
        return True
    return False
def checkoutTimeNigt(from1):
    if ((int(from1[0:2])>=17 and int(from1[0:2])<24) or int(from1[0:2])<=12):
        return True
    return False
def checkoutTimeFromAmToAm(from1,to1,tommorrow=False):
    if ((int(from1[0:2])<=12 and int(from1[0:2])>=5) or (int(from1[0:2])>12 and int(from1[0:2])%12>0 and int(from1[0:2])%12<=3)) and \
        ((int(to1[0:2])<=12 and int(to1[0:2])>=5) or (int(to1[0:2])>12 and int(to1[0:2])%12>0 and int(to1[0:2])%12<=3)):
        if int(from1[0:2])<12 and int(from1[0:2])%12>0 and int(from1[0:2])%12<=3:
           from1=str(int(from1[0:2])+12)+from1[2:]
        if int(to1[0:2])<12 and int(to1[0:2])%12>0 and int(to1[0:2])%12<=3:
           to1=str(int(to1[0:2])+12)+to1[2:]
        if tommorrow:
           to1=str(int(to1[0:2])+24)+to1[2:]
        return True,from1,to1
    else:
        return False,from1,to1
def checkoutTimeFromAmToPm(from1,to1,tommorrow=False):
    if ((int(from1[0:2])<=12 and int(from1[0:2])>=5) or (int(from1[0:2])>12 and int(from1[0:2])%12>0 and int(from1[0:2])%12<=3)) and \
        (int(to1[0:2])%12>0 and int(to1[0:2])%12<=7):
        if int(from1[0:2])<12 and int(from1[0:2])%12>0 and int(from1[0:2])%12<=3:
           from1=str(int(from1[0:2])+12)+from1[2:]
        if int(to1[0:2])<12 and int(to1[0:2])%12>0 and int(to1[0:2])%12<=7:
           to1=str(int(to1[0:2])+12)+to1[2:]
        if tommorrow:
           to1=str(int(to1[0:2])+24)+to1[2:]
        return True,from1,to1
    else:
        return False,from1,to1
def checkoutTimeFromAmToNigt(from1,to1):
    if ((int(from1[0:2])<=12 and int(from1[0:2])>=5) or (int(from1[0:2])>12 and int(from1[0:2])%12>0 and int(from1[0:2])%12<=3)) and \
        ((int(to1[0:2])>=17 and int(to1[0:2])<24) or int(to1[0:2])<=12):
        if int(from1[0:2])<12 and int(from1[0:2])%12>0 and int(from1[0:2])%12<=3:
           from1=str(int(from1[0:2])+12)+from1[2:]
        if int(to1[0:2])==12:
           to1="00"+to1[2:]
        if int(to1[0:2])>=0 and int(to1[0:2])<5:
           to1=str(int(to1[0:2])+24)+to1[2:]
        elif int(to1[0:2])>=5 and int(to1[0:2])<12:
           to1=str(int(to1[0:2])+12)+to1[2:]
        return True,from1,to1
    else:
        return False,from1,to1
def checkoutTimeFromPmToAm(from1,to1):
    if (int(from1[0:2])%12>0 and int(from1[0:2])%12<=7) and\
        ((int(to1[0:2])<=12 and int(to1[0:2])>=5) or (int(to1[0:2])>12 and int(to1[0:2])%12>0 and int(to1[0:2])%12<=3)):
        if int(from1[0:2])<12 and int(from1[0:2])%12>0 and int(from1[0:2])%12<=7:
           from1=str(int(from1[0:2])+12)+from1[2:]
        #由于从下午睡到上午，肯定已经是第二天了，所以要加24
        to1=str(int(to1[0:2])+24)+to1[2:]
        return True,from1,to1
    else:
        return False,from1,to1      
def checkoutTimeFromPmToPm(from1,to1,tommorrow=False):
    if (int(from1[0:2])%12>0 and int(from1[0:2])%12<=7) and\
        (int(to1[0:2])%12>0 and int(to1[0:2])%12<=7):
        if int(from1[0:2])<12 and int(from1[0:2])%12>0 and int(from1[0:2])%12<=7:
           from1=str(int(from1[0:2])+12)+from1[2:]
        if int(to1[0:2])<12 and int(to1[0:2])%12>0 and int(to1[0:2])%12<=7:
           to1=str(int(to1[0:2])+12)+to1[2:]
        if tommorrow:
           to1=str(int(to1[0:2])+24)+to1[2:]
        return True,from1,to1
    else:
        return False,from1,to1      
    
def checkoutTimeFromPmToNigt(from1,to1):
    if (int(from1[0:2])%12>0 and int(from1[0:2])%12<=7) and\
        ((int(to1[0:2])>=17 and int(to1[0:2])<24) or int(to1[0:2])<=12):
        if int(from1[0:2])<12 and int(from1[0:2])%12>0 and int(from1[0:2])%12<=7:
           from1=str(int(from1[0:2])+12)+from1[2:]
        if int(to1[0:2])==12:
           to1="00"+to1[2:]
        if int(to1[0:2])>=0 and int(to1[0:2])<5:
           to1=str(int(to1[0:2])+24)+to1[2:]
        elif int(to1[0:2])>=5 and int(to1[0:2])<12:
           to1=str(int(to1[0:2])+12)+to1[2:]
        return True,from1,to1
    else:
        return False,from1,to1      
    
def checkoutTimeFromNigtToAm(from1,to1):
    if ((int(from1[0:2])>=17 and int(from1[0:2])<24) or int(from1[0:2])<=12) and\
       ((int(to1[0:2])<=12 and int(to1[0:2])>=5) or (int(to1[0:2])>12 and int(to1[0:2])%12>0 and int(to1[0:2])%12<=3)):
        if int(from1[0:2])==12:
           from1="00"+from1[2:]
        if int(from1[0:2])>=0 and int(from1[0:2])<5:
           from1=str(int(from1[0:2])+24)+from1[2:]
        elif int(from1[0:2])>=5 and int(from1[0:2])<12:
           from1=str(int(from1[0:2])+12)+from1[2:]
        if int(to1[0:2])<12 and int(to1[0:2])%12>0 and int(to1[0:2])%12<=3:
           to1=str(int(to1[0:2])+12)+to1[2:]     
        to1=str(int(to1[0:2])+24)+to1[2:]
        return True,from1,to1
    else:
        return False,from1,to1      
def checkoutTimeFromNigtToPm(from1,to1):
    if ((int(from1[0:2])>=17 and int(from1[0:2])<24) or int(from1[0:2])<=12) and\
       (int(to1[0:2])%12>0 and int(to1[0:2])%12<=7):
        if int(from1[0:2])==12:
           from1="00"+from1[2:]
        if int(from1[0:2])>=0 and int(from1[0:2])<5:
           from1=str(int(from1[0:2])+24)+from1[2:]
        elif int(from1[0:2])>=5 and int(from1[0:2])<12:
           from1=str(int(from1[0:2])+12)+from1[2:]
        if int(to1[0:2])<12 and int(to1[0:2])%12>0 and int(to1[0:2])%12<=7:
           to1=str(int(to1[0:2])+12)+to1[2:]
        to1=str(int(to1[0:2])+24)+to1[2:]
        return True,from1,to1
    else:
        return False,from1,to1      
def checkoutTimeFromNigtToNigt(from1,to1,tommorrow=False):
    if ((int(from1[0:2])>=17 and int(from1[0:2])<24) or int(from1[0:2])<=12) and\
       ((int(to1[0:2])>=17 and int(to1[0:2])<24) or int(to1[0:2])<=12):
        if int(from1[0:2])==12:
           from1="00"+from1[2:]
        if int(from1[0:2])>=0 and int(from1[0:2])<5:
           from1=str(int(from1[0:2])+24)+from1[2:]
        elif int(from1[0:2])>=5 and int(from1[0:2])<12:
           from1=str(int(from1[0:2])+12)+from1[2:]
        if int(to1[0:2])==12:
           to1="00"+to1[2:]
        if int(to1[0:2])>=0 and int(to1[0:2])<5:
           to1=str(int(to1[0:2])+24)+to1[2:]
        elif int(to1[0:2])>=5 and int(to1[0:2])<12:
           to1=str(int(to1[0:2])+12)+to1[2:]
        return True,from1,to1
    else:
        return False,from1,to1 
def checkoutTime(ret,ans,fun,to1="",from1=""):
    if from1=="":
        from0=ret.group("from")
        from1=timeConvert(from0)   
    if to1=="":
        to0=ret.group("to")
        to1=timeConvert(to0)
    suss,from1,to1=fun(from1,to1)
    ans["入睡时间"]=from1       
    ans["起床时间"]=to1 
    if suss:
        sleepTime=calSleepTime(ans)   
        if int(sleepTime.split(":")[0])>=0:
            ans["睡觉时长"]=sleepTime  
def swap(t1, t2):
    return t2, t1                 
def extractMilk(speech,ans):
    infoList=["事件","开始时间","结束时间","用时","喝奶类型","喝奶量","单位"]  
    for  i in infoList:
        ans[i]="-"
    ans["事件"]="喝奶"                  
    # 10点到10点半喝奶10盎司分钟（注：考虑到度断断续续的情况）  10点到10点半喝奶 喝了10盎司分钟
    # 10点喝奶10盎司到10点半   
    # 10点喝奶到10点半  
    # 10点到10点半喝奶                                   
    # 10点喝奶10盎司  10点喝奶10分钟        
    # 10点喝奶100     10点喝奶   
    # 喝奶10盎司  #喝奶10分钟
    # 喝奶10              
    ret,from0,to0,sum0,type0=None,None,None,None,None                    
    if ret==None:
        # case0:10点到10点半喝奶（喝了）10盎司分钟（注：考虑到度断断续续的情况）           
        ret=re.search(r"(?P<from>\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[到至](?P<to>\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[喝喂吃]了?(?P<type>奶粉|奶|母乳)(?P<sum>\d{1,4})(?P<unit>[分钟盎司]{1,2})",speech)
        if ret!=None:            
            from0=ret.group("from")
            from1=timeConvert(from0)   
            ans["开始时间"]=from1     
            to0=ret.group("to")
            to1=timeConvert(to0)  
            ans["结束时间"]=to1         
            sum0=ret.group("sum")
            sum1=sumConvert(sum0)  
            ans["喝奶量"]=sum1  
            unit0=ret.group("unit")
            unit1=unitConvert(unit0)  
            ans["单位"]=unit1                                            
            type0=ret.group("type")
            type1=typeConvert(type0)
            ans["喝奶类型"]=type1
            #确认当前精确时间            
            ansTemp={}
            infoList=["事件","入睡时间","起床时间","睡觉时长"]  
            for  i in infoList:
                ansTemp[i]="-"
            hour,minute=getCurTime()
            hour=int(hour)        
            toTime=int(to1.split(":")[0])
            if (toTime<=hour):
                if toTime<12 and abs(toTime-hour)>abs(toTime+12-hour) and toTime+12<=hour:toTime+=12                            
                to1=str(toTime)+":"+to1.split(":")[1]
                to1=timeConvert(to1)            
                # to1,from1=swap(to1,from1) 
                if ansTemp["睡觉时长"]=="-" and  toTime>=5 and toTime<=14 and checkoutTimeAm(to1):
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ansTemp,checkoutTimeFromAmToAm,to1,from1)
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ansTemp,checkoutTimeFromPmToAm,to1,from1)
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ansTemp,checkoutTimeFromNigtToAm,to1,from1)               
                if ansTemp["睡觉时长"]=="-" and  toTime>=12 and toTime<=19 and  checkoutTimePm(to1):                    
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ansTemp,checkoutTimeFromAmToPm,to1,from1)
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ansTemp,checkoutTimeFromPmToPm,to1,from1) 
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ansTemp,checkoutTimeFromNigtToPm,to1,from1)      
                if ansTemp["睡觉时长"]=="-" and  ((toTime>=17 and toTime<24) or (toTime>=0 and toTime<=7)) and  checkoutTimeNigt(to1):
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ansTemp,checkoutTimeFromAmToNigt,to1,from1) 
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ansTemp,checkoutTimeFromPmToNigt,to1,from1) 
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromNigtToNigt,to1,from1) 
                if ansTemp["睡觉时长"]!="-":
                    ans["开始时间"]=ansTemp["入睡时间"]
                    ans["结束时间"]=ansTemp["起床时间"]
                    ans["用时"]=ansTemp["睡觉时长"]
            elif ans["用时"]=="-":
                sleepTime=calSleepTime(ans)   
                if int(sleepTime.split(":")[0])>=0:
                    ans["用时"]=sleepTime              
    if ret==None:
        # case1:10点喝奶10盎司到10点半  case1:10点喝奶到10点半  
        ret=re.search(r"(?P<from>\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[喝喂吃]了?(?P<type>奶粉|奶|母乳)(?P<sum>\d{1,4})?(?P<unit>[分钟盎司]{1,2})?[到至](?P<to>\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:            
            from0=ret.group("from")
            from1=timeConvert(from0)   
            ans["开始时间"]=from1     
            to0=ret.group("to")
            to1=timeConvert(to0)  
            ans["结束时间"]=to1         
            sum0=ret.group("sum")
            sum1=sumConvert(sum0)  
            ans["喝奶量"]=sum1  
            unit0=ret.group("unit")
            unit1=unitConvert(unit0)  
            ans["单位"]=unit1                                            
            type0=ret.group("type")
            type1=typeConvert(type0)
            ans["喝奶类型"]=type1
            #确认当前精确时间            
            ansTemp={}
            infoList=["事件","入睡时间","起床时间","睡觉时长"]  
            for  i in infoList:
                ansTemp[i]="-"
            hour,minute=getCurTime()
            hour=int(hour)        
            toTime=int(to1.split(":")[0])
            if (toTime<=hour):
                if toTime<12 and abs(toTime-hour)>abs(toTime+12-hour) and toTime+12<=hour:toTime+=12                            
                to1=str(toTime)+":"+to1.split(":")[1]
                to1=timeConvert(to1)            
                # to1,from1=swap(to1,from1) 
                if ansTemp["睡觉时长"]=="-" and  toTime>=5 and toTime<=14 and checkoutTimeAm(to1):
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ansTemp,checkoutTimeFromAmToAm,to1,from1)
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ansTemp,checkoutTimeFromPmToAm,to1,from1)
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ansTemp,checkoutTimeFromNigtToAm,to1,from1)               
                if ansTemp["睡觉时长"]=="-" and  toTime>=12 and toTime<=19 and  checkoutTimePm(to1):                    
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ansTemp,checkoutTimeFromAmToPm,to1,from1)
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ansTemp,checkoutTimeFromPmToPm,to1,from1) 
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ansTemp,checkoutTimeFromNigtToPm,to1,from1)      
                if ansTemp["睡觉时长"]=="-" and  ((toTime>=17 and toTime<24) or (toTime>=0 and toTime<=7)) and  checkoutTimeNigt(to1):
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ansTemp,checkoutTimeFromAmToNigt,to1,from1) 
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ansTemp,checkoutTimeFromPmToNigt,to1,from1) 
                    if ansTemp["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromNigtToNigt,to1,from1) 
                if ansTemp["睡觉时长"]!="-":
                    ans["开始时间"]=ansTemp["入睡时间"]
                    ans["结束时间"]=ansTemp["起床时间"]
                    ans["用时"]=ansTemp["睡觉时长"]   
            elif ans["用时"]=="-":
                sleepTime=calSleepTime(ans)   
                if int(sleepTime.split(":")[0])>=0:
                    ans["用时"]=sleepTime  
                
    if ret==None:
        # case3:10点喝奶10盎司  # case4:10点喝奶10分钟  # case5:10点喝奶100     # case6:10点喝奶   
        ret=re.search(r"(?P<from>从?\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[喝喂吃]了?(?P<type>奶粉|奶|母乳)(?P<sum>\d{1,4})?(?P<unit>[分钟盎司]{1,2})?",speech)
        if ret!=None:
            hour,minute=getCurTime()
            hour=int(hour)        
            from0=ret.group("from")
            from1=timeConvert(from0)                  
            fromTime=int(from1.split(":")[0])*60+int(from1.split(":")[1])
            fromTime0=int(from1.split(":")[0])
            sum0=ret.group("sum")
            sum1=sumConvert(sum0)  
            ans["喝奶量"]=sum1  
            unit0=ret.group("unit")
            unit1=unitConvert(unit0)  
            ans["单位"]=unit1                                            
            type0=ret.group("type")
            type1=typeConvert(type0)
            ans["喝奶类型"]=type1
            if (fromTime<=hour*60+int(minute)):   
                if fromTime0<12 and abs(fromTime0-hour)>abs(fromTime0+12-hour) and fromTime0+12<=hour:fromTime0+=12                            
                fromTime=str(fromTime0)+":"+from1.split(":")[1]
                fromTime=timeConvert(fromTime)                                       
                ans["开始时间"]=fromTime                                             
                ans["开始时间"]=fromTime                  
    if ret==None:
        # case7:喝奶10盎司  # case8:喝奶10分钟
        ret=re.search(r"[喝喂吃]了?(?P<type>奶粉|奶|母乳)(?P<sum>\d{1,4})?(?P<unit>[分钟盎司]{1,2})?",speech)
        if ret!=None:      
            sum0=ret.group("sum")
            sum1=sumConvert(sum0)  
            ans["喝奶量"]=sum1  
            unit0=ret.group("unit")
            unit1=unitConvert(unit0)  
            ans["单位"]=unit1                                            
            type0=ret.group("type")
            type1=typeConvert(type0)
            ans["喝奶类型"]=type1
            hour,minute=getCurTime()                                           
            ans["开始时间"]=":".join([hour,minute])                                                                                                   
def extractSleep(speech,ans):
    infoList=["事件","入睡时间","起床时间","睡觉时长"]  
    for  i in infoList:
        ans[i]="-"
    ans["事件"]="睡觉"  
    # 上午
    # 下午
    # 晚上
    ret,from0,to0,sum0,type0=None,None,None,None,None  
###########################################################提取上午起始信息start########################################################################                      
    if ret==None:
        #上午8点睡到了上午9点
        ret=re.search(r"(?P<from>从?(早上?|上午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)睡[到至]了?(?P<to>(早上?|[正上中]午?)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)
        #上午8点睡上午9点起
        if ret==None:
            ret=re.search(r"(?P<from>从?(早上?|上午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉?|入睡).*(?P<to>(早上?|正上中]午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[起|床|醒]",speech)
        #上午8点睡  睡到了上午9点起
        if ret==None:
            ret=re.search(r"(?P<from>从?(早上?|上午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉?|入睡).*睡[到至]了?(?P<to>(早上?|正上中]午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)            
        if ret!=None :
           checkoutTime(ret,ans,checkoutTimeFromAmToAm)
    if ret==None:
        #上午8点睡到下午2点
        ret=re.search(r"(?P<from>从?(早上?|上午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)睡[到至]了?(?P<to>(午后|下午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None :
           checkoutTime(ret,ans,checkoutTimeFromAmToPm)
    if ret==None:
       #早上9点睡觉 下午2点起床
        ret=re.search(r"(?P<from>从?(早上?|上午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉?|入睡).*(?P<to>(午后|下午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[起|床|醒]",speech)
        if ret!=None:
            checkoutTime(ret,ans,checkoutTimeFromAmToPm)               
    if ret==None:
       #上午8点睡到晚上8点
        ret=re.search(r"(?P<from>从?(早上?|上午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)睡[到至]了?(?P<to>(晚上?|黑夜|夜晚)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            checkoutTime(ret,ans,checkoutTimeFromAmToAm)  
    if ret==None:
       #早上9点睡觉 晚上2点起床
        ret=re.search(r"(?P<from>从?(早上?|上午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉?|入睡).*(?P<to>(晚上?|黑夜|夜晚)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[起|床|醒]",speech)
        if ret!=None:
            checkoutTime(ret,ans,checkoutTimeFromAmToPm)   
    if ret==None:
       #上午10点睡的 睡了1个小时10分钟
        ret=re.search(r"(?P<from>从?(早上?|上午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉|睡的|入睡|睡觉).*(?P<to>(睡了)\d{1,2}个?半?(点|小时)?(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            from0=ret.group("from")
            from1=timeConvert(from0)          
            to0=ret.group("to")
            to1=timeConvert(to0)
            fromTime=int(from1.split(":")[0])*60+int(from1.split(":")[1])
            toTime=fromTime+int(to1.split(":")[0])*60+int(to1.split(":")[1])
            to1=str(int((toTime)//60))+":"+str(int((toTime)%60))
            to1=timeConvert(to1)  
            if ans["睡觉时长"]=="-" and  checkoutTimeAm(to1):
                checkoutTime(ret,ans,checkoutTimeFromAmToAm,to1) 
            if ans["睡觉时长"]=="-" and  checkoutTimePm(to1):
                checkoutTime(ret,ans,checkoutTimeFromAmToPm,to1) 
            if ans["睡觉时长"]=="-" and  checkoutTimeNigt(to1):
                checkoutTime(ret,ans,checkoutTimeFromAmToNigt,to1)             
    if ret==None:
       #上午10点醒的 睡了1个小时10分钟
        ret=re.search(r"(?P<from>从?(早上?|上午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[醒起]来?床?的?.*(?P<to>(睡了)\d{1,2}个?半?(点|小时)?(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            from0=ret.group("from")
            from1=timeConvert(from0)          
            to0=ret.group("to")
            to1=timeConvert(to0)
            fromTime=int(from1.split(":")[0])*60+int(from1.split(":")[1])
            toTime=fromTime-(int(to1.split(":")[0])*60+int(to1.split(":")[1]))
            to1=str(int((toTime)//60))+":"+str(int((toTime)%60))
            to1=timeConvert(to1)            
            to1,from1=swap(to1,from1)
            if ans["睡觉时长"]=="-" and  checkoutTimeAm(to1):
                checkoutTime(ret,ans,checkoutTimeFromAmToAm,to1,from1) 
            if ans["睡觉时长"]=="-" and  checkoutTimePm(to1):
                checkoutTime(ret,ans,checkoutTimeFromAmToPm,to1,from1) 
            if ans["睡觉时长"]=="-" and  checkoutTimeNigt(to1):
                checkoutTime(ret,ans,checkoutTimeFromAmToNigt,to1,from1)                                                                 
    if ret==None:
       #早上9点睡到10点
        ret=re.search(r"(?P<from>从?(早上?|上午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)睡[到至]了?(?P<to>\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            from0=ret.group("from")
            from1=timeConvert(from0)                    
            to0=ret.group("to")
            to1=timeConvert(to0)
            if ans["睡觉时长"]=="-" and  checkoutTimeAm(to1):
                checkoutTime(ret,ans,checkoutTimeFromAmToAm) 
            if ans["睡觉时长"]=="-" and  checkoutTimePm(to1):
                checkoutTime(ret,ans,checkoutTimeFromAmToPm) 
            if ans["睡觉时长"]=="-" and  checkoutTimeNigt(to1):
                checkoutTime(ret,ans,checkoutTimeFromAmToNigt) 
##############################################################提取上午起始信息end#######################################################################                
##############################################################提取下午起始信息start#######################################################################                
    if ret==None:
        #下午8点睡到上午9点
        ret=re.search(r"(?P<from>从?(午后|下午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)睡[到至]了?(?P<to>(早上?|[正上中]午?)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None :
           checkoutTime(ret,ans,checkoutTimeFromPmToAm)
    if ret==None:
       #下午9点睡觉 早上10点起床
        ret=re.search(r"(?P<from>从?(午后|下午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉?|入睡).*(?P<to>(早上?|正上中]午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[起|床|醒]",speech)
        if ret!=None:
            checkoutTime(ret,ans,checkoutTimeFromPmToAm)     
    if ret==None:
        #下午8点睡到下午2点
        ret=re.search(r"(?P<from>从?(午后|下午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)睡[到至]了?(?P<to>(午后|下午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None :
           checkoutTime(ret,ans,checkoutTimeFromPmToPm)
    if ret==None:
       #下午9点睡觉 下午2点起床
        ret=re.search(r"(?P<from>从?(午后|下午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉?|入睡).*(?P<to>(午后|下午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[起|床|醒]",speech)
        if ret!=None:
            checkoutTime(ret,ans,checkoutTimeFromPmToPm)               
    if ret==None:
       #下午8点睡到晚上8点
        ret=re.search(r"(?P<from>从?(午后|下午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)睡[到至]了?(?P<to>(晚上?|黑夜|夜晚)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            checkoutTime(ret,ans,checkoutTimeFromPmToNigt)  
    if ret==None:
       #下午9点睡觉 晚上2点起床
        ret=re.search(r"(?P<from>从?(午后|下午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉?|入睡).*(?P<to>(晚上?|黑夜|夜晚)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[起|床|醒]",speech)
        if ret!=None:
            checkoutTime(ret,ans,checkoutTimeFromPmToNigt)   
    if ret==None:
       #下午10点睡的 睡了1个小时10分钟
        ret=re.search(r"(?P<from>从?(午后|下午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉|睡的|入睡|睡觉).*(?P<to>(睡了)\d{1,2}个?半?(点|小时)?(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            from0=ret.group("from")
            from1=timeConvert(from0)          
            to0=ret.group("to")
            to1=timeConvert(to0)
            fromTime=int(from1.split(":")[0])*60+int(from1.split(":")[1])
            toTime=fromTime+int(to1.split(":")[0])*60+int(to1.split(":")[1])
            to1=str(int((toTime)//60))+":"+str(int((toTime)%60))
            to1=timeConvert(to1)  
            if ans["睡觉时长"]=="-" and  checkoutTimePm(to1):
                checkoutTime(ret,ans,checkoutTimeFromPmToPm,to1) 
            if ans["睡觉时长"]=="-" and  checkoutTimeNigt(to1):
                checkoutTime(ret,ans,checkoutTimeFromPmToNigt,to1) 
            if ans["睡觉时长"]=="-" and  checkoutTimeAm(to1):
                checkoutTime(ret,ans,checkoutTimeFromPmToAm,to1)            
    if ret==None:
       #下午10点醒的 睡了1个小时10分钟
        ret=re.search(r"(?P<from>从?(午后|下午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[醒起]来?床?的?.*(?P<to>(睡了)\d{1,2}个?半?(点|小时)?(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            from0=ret.group("from")
            from1=timeConvert(from0)          
            to0=ret.group("to")
            to1=timeConvert(to0)
            fromTime=int(from1.split(":")[0])*60+int(from1.split(":")[1])
            toTime=fromTime-(int(to1.split(":")[0])*60+int(to1.split(":")[1]))
            to1=str(int((toTime)//60))+":"+str(int((toTime)%60))
            to1=timeConvert(to1)            
            to1,from1=swap(to1,from1)
            if ans["睡觉时长"]=="-" and  checkoutTimePm(to1):
                checkoutTime(ret,ans,checkoutTimeFromPmToPm,to1,from1) 
            if ans["睡觉时长"]=="-" and  checkoutTimeNigt(to1):
                checkoutTime(ret,ans,checkoutTimeFromPmToNigt,to1,from1)    
            if ans["睡觉时长"]=="-" and  checkoutTimeAm(to1):
                checkoutTime(ret,ans,checkoutTimeFromPmToAm,to1,from1)                                                              
    if ret==None:
       #下午9点睡到10点
        ret=re.search(r"(?P<from>从?(午后|下午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)睡[到至]了?(?P<to>\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            from0=ret.group("from")
            from1=timeConvert(from0)                    
            to0=ret.group("to")
            to1=timeConvert(to0)           
            if ans["睡觉时长"]=="-" and  checkoutTimePm(to1):
                checkoutTime(ret,ans,checkoutTimeFromPmToPm) 
            if ans["睡觉时长"]=="-" and  checkoutTimeNigt(to1):
                checkoutTime(ret,ans,checkoutTimeFromPmToNigt)   
            if ans["睡觉时长"]=="-" and  checkoutTimeAm(to1):
                checkoutTime(ret,ans,checkoutTimeFromPmToAm)   
##############################################################提取下午起始信息end#######################################################################                
##############################################################提取晚上起始信息start#######################################################################                
    if ret==None:
        #晚上8点睡到上午9点
        ret=re.search(r"(?P<from>从?(晚上?|黑夜|夜晚)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)睡[到至]了?(?P<to>(早上?|[正上中]午?)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None :
           checkoutTime(ret,ans,checkoutTimeFromNigtToAm)
    if ret==None:
       #晚上9点睡觉 早上10点起床
        ret=re.search(r"(?P<from>从?(晚上?|黑夜|夜晚)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉?|入睡).*(?P<to>(早上?|正上中]午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[起|床|醒]",speech)
        if ret!=None:
            checkoutTime(ret,ans,checkoutTimeFromNigtToAm)     
    if ret==None:
        #晚上8点睡到下午2点
        ret=re.search(r"(?P<from>从?(晚上?|黑夜|夜晚)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)睡[到至]了?(?P<to>(午后|下午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None :
           checkoutTime(ret,ans,checkoutTimeFromNigtToPm)
    if ret==None:
       #晚上9点睡觉 下午2点起床
        ret=re.search(r"(?P<from>从?(晚上?|黑夜|夜晚)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉?|入睡).*(?P<to>(午后|下午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[起|床|醒]",speech)
        if ret!=None:
            checkoutTime(ret,ans,checkoutTimeFromNigtToPm)               
    if ret==None:
       #晚上8点睡到晚上9点
        ret=re.search(r"(?P<from>从?(晚上?|黑夜|夜晚)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)睡[到至]了?(?P<to>(晚上?|黑夜|夜晚)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            checkoutTime(ret,ans,checkoutTimeFromNigtToNigt)  
    if ret==None:
       #晚上9点睡觉 晚上2点起床
        ret=re.search(r"(?P<from>从?(晚上?|黑夜|夜晚)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉?|入睡).*(?P<to>(晚上?|黑夜|夜晚)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[起|床|醒]",speech)
        if ret!=None:
            checkoutTime(ret,ans,checkoutTimeFromNigtToNigt)   
    if ret==None:
       #晚上10点睡的 睡了1个小时10分钟
        ret=re.search(r"(?P<from>从?(晚上?|黑夜|夜晚)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉|睡的|入睡|睡觉).*(?P<to>(睡了)\d{1,2}个?半?(点|小时)?(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            from0=ret.group("from")
            from1=timeConvert(from0)          
            to0=ret.group("to")
            to1=timeConvert(to0)
            fromTime=int(from1.split(":")[0])*60+int(from1.split(":")[1])
            toTime=fromTime+int(to1.split(":")[0])*60+int(to1.split(":")[1])
            to1=str(int((toTime)//60))+":"+str(int((toTime)%60))
            to1=timeConvert(to1)  
            if ans["睡觉时长"]=="-" and  checkoutTimePm(to1):
                checkoutTime(ret,ans,checkoutTimeFromNigtToPm,to1) 
            if ans["睡觉时长"]=="-" and  checkoutTimeNigt(to1):
                checkoutTime(ret,ans,checkoutTimeFromNigtToNigt,to1) 
            if ans["睡觉时长"]=="-" and  checkoutTimeAm(to1):
                checkoutTime(ret,ans,checkoutTimeFromNigtToAm,to1)            
    if ret==None:
       #晚上10点醒的 睡了1个小时10分钟
        ret=re.search(r"(?P<from>从?(晚上?|黑夜|夜晚)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[醒起]来?床?的?.*(?P<to>(睡了)\d{1,2}个?半?(点|小时)?(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            from0=ret.group("from")
            from1=timeConvert(from0)          
            to0=ret.group("to")
            to1=timeConvert(to0)
            fromTime=int(from1.split(":")[0])*60+int(from1.split(":")[1])
            toTime=fromTime-(int(to1.split(":")[0])*60+int(to1.split(":")[1]))
            to1=str(int((toTime)//60))+":"+str(int((toTime)%60))
            to1=timeConvert(to1)            
            to1,from1=swap(to1,from1)
            if ans["睡觉时长"]=="-" and  checkoutTimePm(to1):
                checkoutTime(ret,ans,checkoutTimeFromNigtToPm,to1,from1) 
            if ans["睡觉时长"]=="-" and  checkoutTimeNigt(to1):
                checkoutTime(ret,ans,checkoutTimeFromNigtToNigt,to1,from1)    
            if ans["睡觉时长"]=="-" and  checkoutTimeAm(to1):
                checkoutTime(ret,ans,checkoutTimeFromNigtToAm,to1,from1)                                                              
    if ret==None:
       #晚上9点睡到10点
        ret=re.search(r"(?P<from>从?(晚上?|黑夜|夜晚)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)睡[到至]了?(?P<to>\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            from0=ret.group("from")
            from1=timeConvert(from0)                    
            to0=ret.group("to")
            to1=timeConvert(to0)          
            if ans["睡觉时长"]=="-" and  checkoutTimeNigt(to1):
                checkoutTime(ret,ans,checkoutTimeFromNigtToNigt)   
            if ans["睡觉时长"]=="-" and  checkoutTimeAm(to1):
                checkoutTime(ret,ans,checkoutTimeFromNigtToAm)         
            if ans["睡觉时长"]=="-" and  checkoutTimePm(to1):
                checkoutTime(ret,ans,checkoutTimeFromNigtToPm) 
##############################################################提取晚上起始信息end#######################################################################                
##############################################################提取截止起始信息start#######################################################################                
    if ret==None:
       #9点睡到上午8点
        ret=re.search(r"(?P<from>从?\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)睡[到至]了?(?P<to>(早上?|上午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            from0=ret.group("from")
            from1=timeConvert(from0)                    
            to0=ret.group("to")
            to1=timeConvert(to0)
            if ans["睡觉时长"]=="-" and  checkoutTimeAm(from1):
                checkoutTime(ret,ans,checkoutTimeFromAmToAm) 
            if ans["睡觉时长"]=="-" and  checkoutTimePm(from1):
                checkoutTime(ret,ans,checkoutTimeFromPmToAm) 
            if ans["睡觉时长"]=="-" and  checkoutTimeNigt(from1):
                checkoutTime(ret,ans,checkoutTimeFromNigtToAm) 
    if ret==None:
       #9点睡到下午8点
        ret=re.search(r"(?P<from>从?\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)睡[到至]了?(?P<to>(午后|下午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            from0=ret.group("from")
            from1=timeConvert(from0)                    
            to0=ret.group("to")
            to1=timeConvert(to0)
            if ans["睡觉时长"]=="-" and  checkoutTimePm(from1):
                checkoutTime(ret,ans,checkoutTimeFromPmToPm) 
            if ans["睡觉时长"]=="-" and  checkoutTimeAm(from1):
                checkoutTime(ret,ans,checkoutTimeFromAmToPm)            
            if ans["睡觉时长"]=="-" and  checkoutTimeNigt(from1):
                checkoutTime(ret,ans,checkoutTimeFromNigtToPm) 
    if ret==None:
       #9点睡到晚上8点
        ret=re.search(r"(?P<from>从?\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)睡[到至]了?(?P<to>(晚上?|黑夜|夜晚)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            from0=ret.group("from")
            from1=timeConvert(from0)                    
            to0=ret.group("to")
            to1=timeConvert(to0)           
            if ans["睡觉时长"]=="-" and  checkoutTimeNigt(from1):
                checkoutTime(ret,ans,checkoutTimeFromNigtToNigt)                          
            if ans["睡觉时长"]=="-" and  checkoutTimePm(from1):
                checkoutTime(ret,ans,checkoutTimeFromPmToNigt)        
            if ans["睡觉时长"]=="-" and  checkoutTimeAm(from1):
                checkoutTime(ret,ans,checkoutTimeFromAmToNigt)     
##############################################################提取截止起始信息end#######################################################################                
##############################################################提取模糊起止信息start#######################################################################                                  
    if ret==None:
       #10点到11点半睡觉 10点睡觉11点半起床 9点睡到8点
        ret=re.search(r"(?P<from>从?\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[到至](?P<to>\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉?|入睡)",speech)
        if ret==None:
            ret=re.search(r"(?P<from>从?\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉?|入睡)(?P<to>\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[起|床|醒]",speech)
        if ret==None:
            ret=re.search(r"(?P<from>从?\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)睡[到至]了?(?P<to>\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            hour,minute=getCurTime()
            hour=int(hour)        
            from0=ret.group("from")
            from1=timeConvert(from0)                    
            to0=ret.group("to")
            to1=timeConvert(to0)  
            toTime=int(to1.split(":")[0])
            if (toTime<=hour):
                if toTime<12 and abs(toTime-hour)>abs(toTime+12-hour) and toTime+12<=hour:toTime+=12                            
                to1=str(toTime)+":"+to1.split(":")[1]
                to1=timeConvert(to1)            
                # to1,from1=swap(to1,from1) 
                if ans["睡觉时长"]=="-" and  toTime>=5 and toTime<=14 and checkoutTimeAm(to1):
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromAmToAm,to1,from1)
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromPmToAm,to1,from1)
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromNigtToAm,to1,from1)               
                if ans["睡觉时长"]=="-" and  toTime>=12 and toTime<=19 and  checkoutTimePm(to1):                    
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromAmToPm,to1,from1)
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromPmToPm,to1,from1) 
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromNigtToPm,to1,from1)      
                if ans["睡觉时长"]=="-" and  ((toTime>=17 and toTime<24) or (toTime>=0 and toTime<=7)) and  checkoutTimeNigt(to1):
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromAmToNigt,to1,from1) 
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromPmToNigt,to1,from1) 
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromNigtToNigt,to1,from1)                                  
    if ret==None:
       #10点睡的 睡了1个小时
        ret=re.search(r"(?P<from>从?\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉|睡的|入睡|睡觉).*(?P<to>(睡了)\d{1,2}个?半?(点|小时)?(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            hour,minute=getCurTime()
            hour=int(hour)        
            from0=ret.group("from")
            from1=timeConvert(from0)          
            to0=ret.group("to")
            to1=timeConvert(to0)
            fromTime=int(from1.split(":")[0])*60+int(from1.split(":")[1])
            toTime=fromTime+int(to1.split(":")[0])*60+int(to1.split(":")[1])
            to1=str(int((toTime)//60))+":"+str(int((toTime)%60))
            to1=timeConvert(to1)  
            toTime=int(to1.split(":")[0])
            if (toTime*60+int(to1.split(":")[1])<=hour*60+int(minute)):
                if toTime<12 and abs(toTime-hour)>abs(toTime+12-hour) and toTime+12<=hour:toTime+=12                            
                to1=str(toTime)+":"+to1.split(":")[1]
                to1=timeConvert(to1)            
                # to1,from1=swap(to1,from1) 
                if ans["睡觉时长"]=="-" and  toTime>=5 and toTime<=14 and checkoutTimeAm(to1):
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromAmToAm,to1,from1)
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromPmToAm,to1,from1)
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromNigtToAm,to1,from1)               
                if ans["睡觉时长"]=="-" and  toTime>=12 and toTime<=19 and  checkoutTimePm(to1):                    
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromAmToPm,to1,from1)
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromPmToPm,to1,from1) 
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromNigtToPm,to1,from1)      
                if ans["睡觉时长"]=="-" and  ((toTime>=17 and toTime<24) or (toTime>=0 and toTime<=7)) and  checkoutTimeNigt(to1):
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromAmToNigt,to1,from1) 
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromPmToNigt,to1,from1) 
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromNigtToNigt,to1,from1)      
    if ret==None:
       #10点醒的 睡了1个小时
        ret=re.search(r"(?P<from>从?\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)[醒起]来?床?的?.*(?P<to>(睡了)\d{1,2}个?半?(点|小时)?(半|\d{1,2}[分钟]{0,2})?)",speech)
        if ret!=None:
            hour,minute=getCurTime()
            hour=int(hour)        
            from0=ret.group("from")
            from1=timeConvert(from0)          
            to0=ret.group("to")
            to1=timeConvert(to0)
            fromTime=int(from1.split(":")[0])*60+int(from1.split(":")[1])
            toTime=fromTime-(int(to1.split(":")[0])*60+int(to1.split(":")[1]))
            to1=str(int((toTime)//60))+":"+str(int((toTime)%60))
            to1=timeConvert(to1)            
            to1,from1=swap(to1,from1)
            toTime=int(to1.split(":")[0])
            if (toTime*60+int(to1.split(":")[1])<=hour*60+int(minute)):
                if toTime<12 and abs(toTime-hour)>abs(toTime+12-hour) and toTime+12<=hour:toTime+=12                            
                to1=str(toTime)+":"+to1.split(":")[1]
                to1=timeConvert(to1)            
                # to1,from1=swap(to1,from1) 
                if ans["睡觉时长"]=="-" and  toTime>=5 and toTime<=14 and checkoutTimeAm(to1):
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromAmToAm,to1,from1)
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromPmToAm,to1,from1)
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromNigtToAm,to1,from1)               
                if ans["睡觉时长"]=="-" and  toTime>=12 and toTime<=19 and  checkoutTimePm(to1):                    
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromAmToPm,to1,from1)
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromPmToPm,to1,from1) 
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromNigtToPm,to1,from1)      
                if ans["睡觉时长"]=="-" and  ((toTime>=17 and toTime<24) or (toTime>=0 and toTime<=7)) and  checkoutTimeNigt(to1):
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromAmToNigt,to1,from1) 
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromPmToNigt,to1,from1) 
                    if ans["睡觉时长"]=="-":checkoutTime(ret,ans,checkoutTimeFromNigtToNigt,to1,from1)     
    if ret==None:
       #11点睡觉
        ret=re.search(r"(?P<from>从?\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉|睡的|入睡)",speech)
        if ret!=None:
            hour,minute=getCurTime()
            hour=int(hour)        
            from0=ret.group("from")
            from1=timeConvert(from0)          
          
            fromTime=int(from1.split(":")[0])*60+int(from1.split(":")[1])
            fromTime0=int(from1.split(":")[0])
            if (fromTime<=hour*60+int(minute)):   
                if fromTime0<12 and abs(fromTime0-hour)>abs(fromTime0+12-hour) and fromTime0+12<=hour:fromTime0+=12                            
                fromTime=str(fromTime0)+":"+from1.split(":")[1]
                fromTime=timeConvert(fromTime)                                       
                ans["入睡时间"]=fromTime
    if ret==None:
       #11点睡醒
        ret=re.search(r"(?P<to>从?\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡?醒|起床)",speech)
        if ret!=None:
            hour,minute=getCurTime()
            hour=int(hour)        
            to0=ret.group("to")
            to1=timeConvert(to0)                    
            toTime=int(to1.split(":")[0])*60+int(to1.split(":")[1])
            toTime0=int(to1.split(":")[0])
            if (toTime<=hour*60+int(minute)):   
                if toTime0<12 and abs(toTime0-hour)>abs(toTime0+12-hour) and toTime0+12<=hour:toTime0+=12                            
                toTime=str(toTime0)+":"+to1.split(":")[1]
                toTime=timeConvert(toTime)                                       
                ans["起床时间"]=toTime
    if ret==None:
       #睡着了
        ret=re.search(r"(睡着|睡觉|入睡)了?",speech)
        if ret!=None:
            hour,minute=getCurTime()                                           
            ans["入睡时间"]=":".join([hour,minute])    
    if ret==None:
       #睡醒了
        ret=re.search(r"(睡醒|起床)了?",speech)
        if ret!=None:
            hour,minute=getCurTime()
            ans["起床时间"]=":".join([hour,minute])                                                    
    return 0  
def extract(speech): 
    ans={}
    #预处理,去掉空格
    speech=re.sub(r"\s", "",speech)
    speech=re.sub(r"中午|正午", "上午",speech)
    # speech=re.sub(r"\s", "",speech)
    #确认事件     
    if re.search(r"[喝喂吃]了?(奶粉|奶|母乳)", speech):
        errors=extractMilk(speech,ans)
    elif re.search(r"睡[了到醒觉着]了?|起床", speech):
        errors=extractSleep(speech,ans)
    print("errors ", errors)
    print(ans)




if __name__=="__main__":
    info="上午8点睡觉 睡到了下午4点"
    # ret=re.search(r"(?P<from>从?(早上?|上午)\d{1,2}点(半|\d{1,2}[分钟]{0,2})?)(睡觉|睡的|入睡|睡觉)(?P<to>(睡了)\d{1,2}个?半?(点|小时)?(半|\d{1,2}[分钟]{0,2})?)",info)
    # ret=re.search(r"[喝喂吃]了?(?P<type>奶粉|奶|母乳)(?P<sum>\d{1,4}[分钟盎司]{1,3})",info)
    info=extract(info)
    print("eixt")