(function($){"use strict";$(document).ready(function(){$("#cart-wrapper").mCustomScrollbar({theme:"minimal"});$('#cart-dismiss, .cart-overlay').on('click',function(){$('#cart-wrapper').removeClass('active');$('.cart-overlay').fadeOut();});$('.cart-Collapse').on('click',function(){$('#cart-wrapper').addClass('active');$('.cart-overlay').fadeIn();$('.collapse.in').toggleClass('in');$('a[aria-expanded=true]').attr('aria-expanded','false');});});$(function(){$('[data-toggle="tooltip"]').tooltip()});$('.jarallax').jarallax({speed:0.3});$('.toggle-overlay').on('click',function(){$('.search-body').toggleClass('search-open');});$(window).on('scroll',function(){if($(this).scrollTop()>200){$('.backtotop:hidden').stop(true,true).fadeIn();}else{$('.backtotop').stop(true,true).fadeOut();}});$(function(){$(".scroll").on('click',function(){$("html,body").animate({scrollTop:$(".thetop").offset().top},"slow");return false})});$(window).on('load',function(){$('#preloader').fadeOut('slow',function(){$(this).remove();});});$('#slider-section').slick({dots:true,fade:true,speed:400,infinite:true,autoplay:true,slidesToShow:1,cssEase:'linear',autoplaySpeed:4000});$('.service-carousel').owlCarousel({items:4,margin:15,nav:false,loop:true});$('#team-testimonial').owlCarousel({items:1,nav:false,margin:30,loop:false});$(document).ready(function(){$('.popup-youtube').magnificPopup({disableOn:700,type:'iframe',preloader:false,removalDelay:160,mainClass:'mfp-fade',fixedContentPos:false});});var mainHeader=$('.cd-auto-hide-header'),secondaryNavigation=$('.cd-secondary-nav'),belowNavHeroContent=$('.sub-nav-hero'),headerHeight=mainHeader.height();var scrolling=false,previousTop=0,currentTop=0,scrollDelta=10,scrollOffset=150;$(window).on('scroll',function(){if(!scrolling){scrolling=true;(!window.requestAnimationFrame)?setTimeout(autoHideHeader,250):requestAnimationFrame(autoHideHeader);}});$(window).on('resize',function(){headerHeight=mainHeader.height();});function autoHideHeader(){var currentTop=$(window).scrollTop();(belowNavHeroContent.length>0)?checkStickyNavigation(currentTop):checkSimpleNavigation(currentTop);previousTop=currentTop;scrolling=false;}
function checkSimpleNavigation(currentTop){if(previousTop-currentTop>scrollDelta){mainHeader.removeClass('is-hidden');}else if(currentTop-previousTop>scrollDelta&&currentTop>scrollOffset){mainHeader.addClass('is-hidden');}}
function checkStickyNavigation(currentTop){var secondaryNavOffsetTop=belowNavHeroContent.offset().top-secondaryNavigation.height()-mainHeader.height();if(previousTop>=currentTop){if(currentTop<secondaryNavOffsetTop){mainHeader.removeClass('is-hidden');secondaryNavigation.removeClass('fixed slide-up');belowNavHeroContent.removeClass('secondary-nav-fixed');}else if(previousTop-currentTop>scrollDelta){mainHeader.removeClass('is-hidden');secondaryNavigation.removeClass('slide-up').addClass('fixed');belowNavHeroContent.addClass('secondary-nav-fixed');}}else{if(currentTop>secondaryNavOffsetTop+scrollOffset){mainHeader.addClass('is-hidden');secondaryNavigation.addClass('fixed slide-up');belowNavHeroContent.addClass('secondary-nav-fixed');}else if(currentTop>secondaryNavOffsetTop){mainHeader.removeClass('is-hidden');secondaryNavigation.addClass('fixed').removeClass('slide-up');belowNavHeroContent.addClass('secondary-nav-fixed');}}};$('.count').each(function(){$(this).prop('Counter',0).animate({Counter:$(this).text()},{duration:5000,easing:'swing',step:function(now){$(this).text(Math.ceil(now));}});});$(document).ready(function(){function setCalculatorValuecoin_calc(){var currencyvalue1old=jQuery(".coin_calc .currencyvalue1").val();var currencyvalue2unit=jQuery(".coin_calc .currency-switcher").val();jQuery(".coin_calc .currencyvalue2").val(currencyvalue1old*currencyvalue2unit);}
function setCalculatorValue2coin_calc(){var currencyvalue2old=jQuery(".coin_calc .currencyvalue2").val();var currencyvalue2unit=jQuery(".coin_calc .currency-switcher").val();jQuery(".coin_calc .currencyvalue1").val(currencyvalue2old/currencyvalue2unit);}
setCalculatorValuecoin_calc();jQuery(".coin_calc .currencyvalue1").keyup(setCalculatorValuecoin_calc);jQuery(".coin_calc .currency-switcher").change(setCalculatorValuecoin_calc);jQuery(".coin_calc .currencyvalue2").keyup(setCalculatorValue2coin_calc);});var chartData=[{"date":"2018-01-01","distance":227,"townSize":25,"latitude":40.71,"duration":408},{"date":"2018-01-02","distance":371,"townSize":14,"latitude":38.89,"duration":482},{"date":"2018-01-03","distance":433,"townSize":6,"latitude":34.22,"duration":562},{"date":"2018-01-04","distance":345,"townSize":7,"latitude":30.35,"duration":379},{"date":"2018-01-05","distance":480,"townSize":10,"latitude":25.83,"duration":501},{"date":"2018-01-06","distance":386,"townSize":7,"latitude":30.46,"duration":443},{"date":"2018-01-07","distance":348,"townSize":10,"latitude":29.94,"duration":405},{"date":"2018-01-08","distance":238,"townSize":16,"latitude":29.76,"duration":309},{"date":"2018-01-09","distance":218,"townSize":17,"latitude":32.8,"duration":287},{"date":"2018-01-10","distance":349,"townSize":11,"latitude":35.49,"duration":485},{"date":"2018-01-11","distance":603,"townSize":10,"latitude":39.1,"duration":890},{"date":"2018-01-12","distance":534,"townSize":18,"latitude":39.74,"duration":810},{"date":"2018-01-13","townSize":12,"distance":425,"duration":670,"latitude":40.75,"alpha":0.4},{"date":"2018-01-14","latitude":36.1,"duration":470,"bulletClass":"lastBullet"},{"date":"2018-01-15"},{"date":"2018-01-16"},{"date":"2018-01-17"},{"date":"2018-01-18"},{"date":"2018-01-19"}];var chart=AmCharts.makeChart("chartdiv",{"type":"serial","theme":"light","dataDateFormat":"YYYY-MM-DD","dataProvider":chartData,"addClassNames":true,"startDuration":1,"color":"#ffffff","marginLeft":0,"categoryField":"date","categoryAxis":{"parseDates":true,"minPeriod":"DD","autoGridCount":false,"gridCount":50,"gridAlpha":0.1,"gridColor":"#ffffff","axisColor":"#ffffff","dateFormats":[{"period":'DD',"format":'DD'},{"period":'WW',"format":'MMM DD'},{"period":'MM',"format":'MMM'},{"period":'YYYY',"format":'YYYY'}]},"valueAxes":[{"id":"a1","gridAlpha":0,"axisAlpha":0},{"id":"a2","position":"right","gridAlpha":0,"axisAlpha":0,"labelsEnabled":false},{"id":"a3","position":"right","gridAlpha":0,"axisAlpha":0,"inside":true,"duration":"mm","durationUnits":{"DD":"","hh":"","mm":"","ss":""}}],"graphs":[{"id":"g1","valueField":"distance","title":"Sales Statistic","type":"column","fillAlphas":0.9,"valueAxis":"a1","balloonText":"[[value]] $","legendValueText":"[[value]] Items","legendPeriodValueText":"total: [[value.sum]] items","lineColor":"#ffc107","alphaField":"alpha"},{"id":"g2","valueField":"latitude","classNameField":"bulletClass","title":"Total Balance","type":"line","valueAxis":"a2","lineColor":"#ffffff","lineThickness":1,"legendValueText":"[[value]]/[[description]]","bullet":"round","bulletSizeField":"townSize","bulletBorderColor":"#ffffff","bulletBorderAlpha":1,"bulletBorderThickness":2,"bulletColor":"#ffc107","labelPosition":"right","balloonText":"latitude:[[value]]","showBalloon":true,"animationPlayed":true},{"id":"g3","title":"This Month","valueField":"duration","type":"line","valueAxis":"a3","lineColor":"#ff5755","balloonText":"[[value]]","lineThickness":1,"legendValueText":"[[value]]","bullet":"square","bulletBorderColor":"#ff5755","bulletBorderThickness":1,"bulletBorderAlpha":1,"dashLengthField":"dashLength","animationPlayed":true}],"chartCursor":{"zoomable":false,"categoryBalloonDateFormat":"DD","cursorAlpha":0,"valueBalloonsEnabled":false},"legend":{"bulletType":"round","equalWidths":false,"valueWidth":120,"useGraphSettings":true,"color":"#ffffff"}});function isMobile(){return('ontouchstart'in document.documentElement);}
function init_gmap(){if(typeof google=='undefined')return;var options={center:[23.7806286,90.2793692],zoom:14,styles:[{elementType:'geometry',stylers:[{color:'#242f3e'}]},{elementType:'labels.text.stroke',stylers:[{color:'#242f3e'}]},{elementType:'labels.text.fill',stylers:[{color:'#746855'}]},{featureType:'administrative.locality',elementType:'labels.text.fill',stylers:[{color:'#d59563'}]},{featureType:'poi',elementType:'labels.text.fill',stylers:[{color:'#d59563'}]},{featureType:'poi.park',elementType:'geometry',stylers:[{color:'#263c3f'}]},{featureType:'poi.park',elementType:'labels.text.fill',stylers:[{color:'#6b9a76'}]},{featureType:'road',elementType:'geometry',stylers:[{color:'#38414e'}]},{featureType:'road',elementType:'geometry.stroke',stylers:[{color:'#212a37'}]},{featureType:'road',elementType:'labels.text.fill',stylers:[{color:'#9ca5b3'}]},{featureType:'road.highway',elementType:'geometry',stylers:[{color:'#746855'}]},{featureType:'road.highway',elementType:'geometry.stroke',stylers:[{color:'#1f2835'}]},{featureType:'road.highway',elementType:'labels.text.fill',stylers:[{color:'#f3d19c'}]},{featureType:'transit',elementType:'geometry',stylers:[{color:'#2f3948'}]},{featureType:'transit.station',elementType:'labels.text.fill',stylers:[{color:'#d59563'}]},{featureType:'water',elementType:'geometry',stylers:[{color:'#17263c'}]},{featureType:'water',elementType:'labels.text.fill',stylers:[{color:'#515c6d'}]},{featureType:'water',elementType:'labels.text.stroke',stylers:[{color:'#17263c'}]}],mapTypeControl:true,mapTypeControlOptions:{style:google.maps.MapTypeControlStyle.DROPDOWN_MENU},navigationControl:true,scrollwheel:false,streetViewControl:true,}
if(isMobile()){options.draggable=false;}
$('#google-map').gmap3({map:{options:options},marker:{latLng:[23.7806286,90.2793692],}});}
init_gmap();})(jQuery);