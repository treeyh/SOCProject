var Common = {
    alert: function (msg, gotoUrl) {
        if (msg != undefined &&  msg != '') {
            alert(msg);
            if (gotoUrl != undefined && gotoUrl != '') {
                window.location.href = gotoUrl;
            }
        }
    },
    confirm : function(msg) {
    	return confirm(msg);
    },
    isNullOrEmpty : function(str){
        if(undefined == str || str == ''){
            return true;
        }
        return false;
    }
};

var DateTime = {
    Sun : 0,
    Mon : 1,
    Tue : 2,
    Wed : 3,
    Thu : 4,
    Fri : 5,
    Sat : 6,
    DayMilliSecond : 86400000,
    getNowDate: function(){
        //获得当前日期
        return DateTime.getDateToStr(new Date());
    },
    getNowDateTime: function(){
        //获得当前日期
        return DateTime.getDateTimeToStr(new Date());
    },
    getDateToStr : function(date){
        // 将日期类型转换成字符串型格式yyyy-MM-dd 
        var Year=0;
        var Month=0;
        var Day=0;
        var CurrentDate="";
        //初始化时间
        Year      = date.getFullYear();
        Month     = date.getMonth()+1;
        Day       = date.getDate();
        CurrentDate = Year + "-" + (Month >= 10 ? '' : '0') + Month + '-' + (Day >= 10 ? '' : '0') + Day;
        return CurrentDate;
    },
    getDateTimeToStr : function(date){
        // 将日期类型转换成字符串型格式yyyy-MM-dd hh:mm
        var Year=0;
        var Month=0;
        var Day=0;
        var Hour = 0;
        var Minute = 0;
        var CurrentDate="";

        //初始化时间
        Year      = DateIn.getFullYear();
        Month     = DateIn.getMonth()+1;
        Day       = DateIn.getDate();
        Hour      = DateIn.getHours();
        Minute    = DateIn.getMinutes();

        CurrentDate = Year + "-" + (Month >= 10 ? '' : '0') + Month + 
                (Day >= 10 ? '' : '0') + Day + (Hour >=10 ? ' ' : ' 0') + Hour +
                (Minute >=10 ? ':' : ':0') + Minute;         
        return CurrentDate;
    },
    parseDate: function(date){
        //从string转换啊为date类型，支持yyyy-MM-dd、yyyy-MM-dd HH:mm、yyyy-MM-dd HH:mm:ss
        return new Date(Date.parse(date.replace(/-/g,   "/")));
    },    
    diffDateCount: function(startDate, endDate, isFilterRest){
        //计算两个日期的相差的天数，
        //startDate 开始日期（yyyy-MM-dd）， endDate 结束日期（yyyy-MM-dd）， isFilterRest是否过滤周六、日
        var start = DateTime.parseDate(startDate);
        var end = DateTime.parseDate(endDate);
        var dayCount = Math.ceil((end.getTime() - start.getTime())/DateTime.DayMilliSecond);
        if(undefined == isFilterRest || (undefined != isFilterRest && isFilterRest == false)){
            return dayCount;
        }

        var day = 0;
        if(start.getTime() < end.getTime()){
            day = DateTime.restDateCount(start, end);
            dayCount = dayCount - day;
        }else{
            day = DateTime.restDateCount(end, start);
            dayCount = dayCount + day;
        }
        return dayCount;//进一法取整
    },
    restDateCount: function(start, end){
        //计算两个日期之间的休息日天数。
        //参数为date类型
        var days = Math.ceil((end.getTime() - start.getTime()) / DateTime.DayMilliSecond);
        var weekCount = Math.floor(days / 7);
        var restCount = weekCount * 2;

        var rem = days % 7;

        var startDay = start.getDay();
        if(startDay == 0){
            restCount = restCount + 1;
        }
        startDay = startDay + rem;
        if(startDay == 7){
            restCount = restCount + 1;
        }else if(startDay > 7){
            restCount = restCount + 2;
        }
        return restCount;
    },
    getWorkDayCountDate: function(startDate, dayCount){
        //计算一个日期后N天的前一天工作日日期
        //startDate-MM-dd），dayCount：向后N天
        //算法搞不来，只能用笨办法了
        var count = dayCount - 1;
        var start = DateTime.parseDate(startDate);

        while(true){
            if(count <= 0 && (start.getDay() != 0 && start.getDay() != 6)){
                break;
            }
            if(start.getDay() > 0 && start.getDay() < 6){
                count--;
            }
            start.setTime(start.getTime() + DateTime.DayMilliSecond);
        }
        return start;

        // var day = dayCount + Math.floor(dayCount / 7) * 2;
        
        // var start = DateTime.parseDate(startDate);

        // var rem = dayCount % 7;
        // var startDay = start.getDay();
        // if (startDay == 6){
        //     rem = rem + 1;
        // }
        // day = day + rem - 1; //减一是为了前一天
        // var date = new Date();
        // date.setTime(start.getTime() + day * DateTime.DayMilliSecond);

        // return date;


        // var start = DateTime.parseDate(startDate);
        // var pianyi = 0;
        // if(start.getDay() == 0){
        //     pianyi = 1;
        // }else if(start.getDay() == 6){
        //     pianyi = 2;
        // }else{
        //     pianyi = (5 - start.getDay());
        // }

        // var weekCount = Math.floor(dayCount / 5);
        // var weekDayCount = weekCount * 7;

        // var moreDay = dayCount % 5;

        // start.setTime(start.getTime() + (pianyi + 
        //     weekDayCount + moreDay) * DateTime.DayMilliSecond);
        // alert(start);
        // return start;
    }
};