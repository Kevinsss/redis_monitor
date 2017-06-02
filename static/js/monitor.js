var redis_info = 0;
$(function () {
    if (redis_info !== 0)
        clearInterval(redis_info);
    redis_info = setInterval(function () {
        getInfo();
    }, 3000); //每隔3秒刷新
});

var command_count_int = 0;
$(function () {
    $('#commandlast').change(function () {
        var lasted = $(this).val();
        if (command_count_int !== 0)
            clearInterval(command_count_int);
        command_count_int = setInterval(function () {
            getCommandCount(lasted);
        }, 3000); //每隔3秒刷新
    });
    $('#commandlast').trigger("change");
});
var memory_count_int = 0;
$(function () {
    $('#memorylast').change(function () {
        var lasted = $(this).val();
        if (memory_count_int !== 0)
            clearInterval(memory_count_int);
        memory_count_int = setInterval(function () {
            getMemoryCount(lasted);
        }, 3000); //每隔3秒刷新
    });
    $('#memorylast').trigger("change");
});


$(function () {
    $.ajax({
        url: "/api/ip",
        method: 'post',
        success: function (json) {
            var data = eval(json);
            for (var i = 0; i < data.length; i++)
                $('#ip').append("<option value='" + data[i] + "'>" + data[i] + "</option>");

        },
        error: function (xhr) {
        }
    });
});

function getCommandCount(hours) {
    var end = Math.round(new Date().getTime() / 1000);
    var start = end - hours * 60 * 60;  // convert to seconds
    var ip = $('#ip').val();
    var args = {
        "start": start,
        "end": end,
        "ip": ip
    };
    $.ajax({
        url: "/api/commandcount",
        method: 'post',
        data: args,
        success: function (json) {
            var newData = eval(json);
            commandChart.changeData(newData);
        },
        error: function (xhr) {
        }
    });
}

function getMemoryCount(hours) {
    var end = Math.round(new Date().getTime() / 1000);
    var start = end - hours * 60 * 60;  // convert to seconds
    var ip = $('#ip').val();
    var args = {
        "start": start,
        "end": end,
        "ip": ip
    };
    $.ajax({
        url: "/api/memory",
        method: 'post',
        data: args,
        success: function (json) {
            var newData = eval(json);
            memoryChart.changeData(newData);

        },
        error: function (xhr) {
        }
    });
}

function getInfo() {
    var ip = $('#ip').val();
    var args = {
        "ip": ip
    };
    $.ajax({
        url: "/api/info",
        method: 'post',
        dataType: "json",
        data: args,
        success: function (data) {
            $('#uptime').html('<strong>Uptime: xxx</strong>'.replace('xxx', data.uptime));
            $('#maxMemory').html('<strong>Max Memory: xxx</strong>'.replace('xxx', data.max_memory));
            $('#connectedClients').html('<strong>Connected Clients: xxx</strong>'.replace('xxx', data.connnected_clients));
            $('#usedCpuSys').html('<strong>Used CPU Sys: xxx</strong>'.replace('xxx', data.used_cpu_sys));
            $('#usedCpuUser').html('<strong>Used CPU User: xxx</strong>'.replace('xxx', data.used_cpu_user));
            $('#usedMemory').html('<strong>Used Memory: xxx</strong>'.replace('xxx', data.used_memory));
            $('#usedMemoryRss').html('<strong>Used Memory Rss: xxx</strong>'.replace('xxx', data.used_memory_rss));
            $('#usedMemoryPeak').html('<strong>Used Memory Peak: xxx</strong>'.replace('xxx', data.used_memory_peak));
            $('#memRatio').html('<strong>Mem Fragmentation Ratio: xxx</strong>'.replace('xxx', data.mem_fragmentation_ratio));
            $('#totalConnectionReceived').html('<strong>Total Connection Received: xxx</strong>'.replace('xxx', data.total_connection_recevied));
            $('#totalCommadsProcessed').html('<strong>Total Commands Processed: xxx</strong>'.replace('xxx', data.total_commands_processed));
            $('#expiredKeys').html('<strong>Expired Keys: xxx</strong>'.replace('xxx', data.expired_keys));
        },
        error: function (xhr) {
        }
    });
}

function createCommandChart(chart) {


    var defs = {

        'optime': {
            formatter: function (val) {
                return formatDateTime(new Date(val * 1000));
            },
            alias: '操作时间'
        },
        'cmdcount': {
            alias: 'CommandCount'
        }
    };
    chart.source(null, defs);
    // chart.source(null, {
    //     time: {
    //         alias: "时间"
    //     },
    //     value: {
    //         alias: "CommandCount"
    //     }
    // });
    chart.axis('optime', {

        title: {
            fontSize: '20',
            textAlign: 'center'
        }
    });
    // var unixTimestamp = new Date(Unix timestamp * 1000) 然后 commonTime = unixTimestamp.toLocaleString()
    chart.axis('cmdcount', {
        formatter: function (val) {
            if (val > 1000)
                return (val / 1000) + 'K';

        },
        title: {
            fontSize: '20',
            textAlign: 'center'
        }
    });
    chart.line().position('optime*cmdcount').size(3);
    chart.point().position('optime*cmdcount').color('#EB4456').shape('circle').size(3);
    chart.render();
}
function createMemoryChart(chart) {

    var defs = {
        'optime': {
            formatter: function (val) {
                return formatDateTime(new Date(val * 1000));
            },
            alias: '操作时间'
        },
        'used_memory': {
            formatter: function (val) {
                if (val > 1024 * 1024)
                    return (val / 1024 / 1024).toFixed(2) + 'M';
                else if (val > 1024)
                    return (val / 1024).toFixed(2) + 'K';
                else
                    return val + 'B';
            },
            alias: 'UsedMemory'
        },
        'peak_memory': {
            formatter: function (val) {
                if (val > 1024 * 1024)
                    return (val / 1024 / 1024).toFixed(2) + 'M';
                else if (val > 1024)
                    return (val / 1024).toFixed(2) + 'K';
                else
                    return val + 'B';
            },
            alias: 'MaxUsedMemory'
        }

    };

    chart.source(null, defs);

    chart.axis('optime', {

        title: {
            fontSize: '20',
            textAlign: 'center'
        }
    });
    // var unixTimestamp = new Date(Unix timestamp * 1000) 然后 commonTime = unixTimestamp.toLocaleString()
    chart.axis('used_memory', {

        title: {
            fontSize: '20',
            textAlign: 'center'
        }
    });
    chart.axis('peak_memory', {
        title: null,
        line: null,
        tickLine: null,
        labels: null
    });
    chart.legend({
        position: 'top', // 设置图例的显示位置
        dy: -20

    });
    chart.area().position('optime*used_memory');
    chart.line().position('optime*peak_memory').color('#F9815C').shape('dash').size(2);
    chart.point().position('optime*peak_memory').color('#EB4456').shape('circle').size(3);
    chart.render();
}

function formatDateTime(inputTime) {
    var date = new Date(inputTime);
    var y = date.getFullYear();
    var m = date.getMonth() + 1;
    m = m < 10 ? ('0' + m) : m;
    var d = date.getDate();
    d = d < 10 ? ('0' + d) : d;
    var h = date.getHours();
    h = h < 10 ? ('0' + h) : h;
    var minute = date.getMinutes();
    var second = date.getSeconds();
    minute = minute < 10 ? ('0' + minute) : minute;
    second = second < 10 ? ('0' + second) : second;
    return y + '/' + m + '/' + d + ' ' + h + ':' + minute + ':' + second;
}
