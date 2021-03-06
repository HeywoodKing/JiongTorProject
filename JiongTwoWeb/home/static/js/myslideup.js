// JavaScript Document
(function($){
	$.fn.extend({
		"slideUp": function(value){
			
			var docthis = this;
			//默认参数
			value = $.extend({
				 "height": "30",
				 "retentiontime": 2000,
				 "movetime": 1000
			}, value)
			
			//向上滑动动画
			function autoani(){
				// 在文档docthis中，查找取出第一个li元素。
				$("li:first", docthis).animate({"margin-top": -value.height}, value.movetime, function(){
					$(this).css("margin-top", 0).appendTo(".rolling-news");
				});
			}
			
			//自动间隔时间向上滑动
			var anifun = setInterval(autoani, value.retentiontime);
			
			//悬停时停止滑动，离开时继续执行
			$(docthis).children("li").hover(function(){
				clearInterval(anifun);			//清除自动滑动动画
			}, function(){
				anifun = setInterval(autoani, value.retentiontime);	//继续执行动画
			})
		}	
	});
})(jQuery)