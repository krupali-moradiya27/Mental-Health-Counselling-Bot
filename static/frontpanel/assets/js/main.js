/***************************************************
==================== JS INDEX ======================
****************************************************
01. PreLoader Js
02. Info Bar Js
03. Data-Background Js
04. Sticky Header Js
05. Mobile Menu Js
06. Scroll To Top Js
07. Hero Slider Js
08. Case Slider Js
09. Client Slider Js
10. Testimonial Slider Js
11. Testimonial Slider 2 Js
12. Testimonial Slider 3 Js
13. Award Slider Js
14. Team Achivement Slider Js
15. Project Slider Js
16. Post Box Slider Js
17. Masonary Js
18. Nice Select Js
19. WoW Js
20. Counter Js
****************************************************/

(function ($) {
"use strict";

	////////////////////////////////////////////////////
    // 01. PreLoader Js
	$(window).on('load',function() {
		$("#loading").fadeOut(500);
	});


	////////////////////////////////////////////////////
    // 02. Info Bar Js
	$(".info-toggle-btn").on("click", function () {
		$(".info__area").addClass("info-opened");
		$(".body-overlay").addClass("opened");
	});
	$(".info-close-btn").on("click", function () {
		$(".info__area").removeClass("info-opened");
		$(".body-overlay").removeClass("opened");
	});
	$(".body-overlay").on("click", function () {
		$(".info__area").removeClass("info-opened");
		$(".body-overlay").removeClass("opened");
	});

	
	////////////////////////////////////////////////////
    // 03. Sticky Header Js
	$(window).on('scroll', function () {
		var scroll = $(window).scrollTop();
		if (scroll < 100) {
			$("#header-sticky").removeClass("sticky");
		} else {
			$("#header-sticky").addClass("sticky");
		}
	});
	


	////////////////////////////////////////////////////
    // 04. Data-Background Js
	$("[data-background").each(function () {
		$(this).css("background-image", "url( " + $(this).attr("data-background") + "  )");
	});

	
	////////////////////////////////////////////////////
    // 05. Mobile Menu Js
	$('#mobile-menu-active').metisMenu();

	$('#mobile-menu-active .has-dropdown > a').on('click', function (e) {
		e.preventDefault();
	});

	////////////////////////////////////////////////////
    // 06. Scroll To Top Js
	function smoothSctollTop() {
		$('.smooth-scroll a').on('click', function (event) {
			var target = $(this.getAttribute('href'));
			if (target.length) {
				event.preventDefault();
				$('html, body').stop().animate({
					scrollTop: target.offset().top - 0
				}, 1500);
			}
		});
	}
	smoothSctollTop();

	// Show or hide the sticky footer button
	$(window).on('scroll', function(event) {
		if($(this).scrollTop() > 600){
			$('#scroll').fadeIn(200)
		} else{
			$('#scroll').fadeOut(200)
		}
	});

	//Animate the scroll to yop
	$('#scroll').on('click', function(event) {
		event.preventDefault();

		$('html, body').animate({
			scrollTop: 0,
		}, 1500);
	});

	////////////////////////////////////////////////////
    // 07. Hero Slider Js
	function mainSlider() {
	var BasicSlider = $('.slider-active');
	BasicSlider.on('init', function (e, slick) {
		var $firstAnimatingElements = $('.single-slider:first-child').find('[data-animation]');
		doAnimations($firstAnimatingElements);
	});
	BasicSlider.on('beforeChange', function (e, slick, currentSlide, nextSlide) {
		var $animatingElements = $('.single-slider[data-slick-index="' + nextSlide + '"]').find('[data-animation]');
		doAnimations($animatingElements);
	});
	BasicSlider.slick({
		autoplay: true,
		autoplaySpeed: 8000,
		dots: true,
		fade: true,
		arrows: true,
		prevArrow: '<button type="button" class="slick-prev"><i class="fal fa-angle-left"></i></button>',
		nextArrow: '<button type="button" class="slick-next"><i class="fal fa-angle-right"></i></button>',
		responsive: [{
		breakpoint: 767,
		settings: {
			dots: false,
			arrows: false
		}
		}]
	});

	function doAnimations(elements) {
		var animationEndEvents = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
		elements.each(function () {
		var $this = $(this);
		var $animationDelay = $this.data('delay');
		var $animationType = 'animated ' + $this.data('animation');
		$this.css({
			'animation-delay': $animationDelay,
			'-webkit-animation-delay': $animationDelay
		});
		$this.addClass($animationType).one(animationEndEvents, function () {
			$this.removeClass($animationType);
		});
		});
	}
	}
	mainSlider();


	////////////////////////////////////////////////////
    // 08. Case Slider Js
	$('.case__slider-active').slick({
		centerMode: true,
		centerPadding: '0px',
		dots: false,
		arrows: false,
		infinite: true,
		speed: 700,
		slidesToShow: 3,
		slidesToScroll: 1,
		autoplay:false,
		responsive: [
			{
				breakpoint: 1024,
				settings: {
					slidesToShow: 3,
					slidesToScroll: 1,
					infinite: true
				}
			},
			{
				breakpoint: 991,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 1,
					infinite: true
				}
			},
			{
				breakpoint: 767,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
			},
			{
				breakpoint: 576,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
			}
		]
	});

	////////////////////////////////////////////////////
    // 09. Client Slider Js
	$('.client__slider-active').owlCarousel({
		loop:true,
		margin:30,
		autoplay:false,
		autoplayTimeout:3000,
		smartSpeed:500,
		items:6,
		navText:['<button><i class="fa fa-angle-left"></i>PREV</button>','<button>NEXT<i class="fa fa-angle-right"></i></button>'],
		nav:false,
		dots:false,
		responsive:{
			0:{
				items:1
			},
			767:{
				items:2
			},
			992:{
				items:3
			},
			1200:{
				items:4
			},
			1600:{
				items:5
			}
		}
	});

	////////////////////////////////////////////////////
    // 10. Testimonial Slider Js
	$('.testimonial__slider').owlCarousel({
		loop:true,
		margin:30,
		autoplay:false,
		autoplayTimeout:3000,
		smartSpeed:500,
		items:6,
		navText:['<button><i class="far fa-angle-left"></i></button>','<button><i class="far fa-angle-right"></i></button>'],
		nav:true,
		dots:false,
		responsive:{
			0:{
				items:1
			},
			767:{
				items:1
			},
			992:{
				items:2
			},
			1200:{
				items:3
			}
		}
	});


	////////////////////////////////////////////////////
    // 11. Testimonial Slider 2 Js
	$('.testimonial__slider-2-active').owlCarousel({
		loop:true,
		margin:30,
		autoplay:false,
		autoplayTimeout:3000,
		smartSpeed:500,
		items:6,
		navText:['<button><i class="fas fa-angle-left"></i></button>','<button><i class="fas fa-angle-right"></i></button>'],
		nav:true,
		dots:false,
		responsive:{
			0:{
				items:1
			},
			767:{
				items:1
			},
			992:{
				items:2
			}
		}
	});

	////////////////////////////////////////////////////
    // 12. Testimonial Slider 3 Js
	$('.testimonial__slider-3').owlCarousel({
		loop:true,
		margin:0,
		autoplay:false,
		autoplayTimeout:3000,
		smartSpeed:500,
		items:6,
		navText:['<button><i class="fal fa-long-arrow-left"></i></button>','<button><i class="fal fa-long-arrow-right"></i></button>'],
		nav:true,
		dots:false,
		responsive:{
			0:{
				items:1
			},
			767:{
				items:1
			},
			992:{
				items:1
			}
		}
	});

	////////////////////////////////////////////////////
    // 13. Award Slider Js
	$('.award__slider-active').owlCarousel({
		loop:true,
		margin:30,
		autoplay:false,
		autoplayTimeout:3000,
		smartSpeed:500,
		items:6,
		navText:['<button><span class="owl-arrow prev-arrow"></span></button>','<button><span class="owl-arrow next-arrow"></span></button>'],
		nav:true,
		dots:false,
		responsive:{
			0:{
				items:2
			},
			767:{
				items:3
			},
			992:{
				items:3
			},
			1200:{
				items:3
			},
			1600:{
				items:5
			}
		}
	});

	////////////////////////////////////////////////////
    // 14. Team Achivement Slider Js
	$('.team__achivement-slider').owlCarousel({
		loop:true,
		margin:30,
		autoplay:false,
		autoplayTimeout:3000,
		smartSpeed:500,
		items:6,
		navText:['<button><span class="owl-arrow prev-arrow"></span></button>','<button><span class="owl-arrow next-arrow"></span></button>'],
		nav:true,
		dots:false,
		responsive:{
			0:{
				items:2
			},
			767:{
				items:3
			},
			992:{
				items:3
			},
			1200:{
				items:5
			},
			1600:{
				items:5
			}
		}
	});

	////////////////////////////////////////////////////
    // 15. Project Slider Js
	$('.project__slider-active').owlCarousel({
		loop:true,
		margin:20,
		autoplay:false,
		autoplayTimeout:3000,
		smartSpeed:500,
		items:6,
		navText:['<button><i class="fal fa-angle-left"></i></button>','<button><i class="fal fa-angle-right"></i></button>'],
		nav:true,
		dots:false,
		responsive:{
			0:{
				items:1
			},
			767:{
				items:2
			},
			992:{
				items:2
			},
			1200:{
				items:3
			},
			1600:{
				items:4
			}
		}
	});

	////////////////////////////////////////////////////
    // 16. Post Box Slider Js
	$('.postbox__gallery').owlCarousel({
		loop:true,
		margin:0,
		autoplay:false,
		autoplayTimeout:3000,
		smartSpeed:500,
		items:6,
		navText:['<button><i class="far fa-arrow-left"></i></button>','<button><i class="far fa-arrow-right"></i></button>'],
		nav:true,
		dots:false,
		responsive:{
			0:{
				items:1
			},
			767:{
				items:1
			},
			992:{
				items:1
			}
		}
	});

	////////////////////////////////////////////////////
    // 17. Masonary Js
	$('.grid').imagesLoaded( function() {
		// init Isotope
		var $grid = $('.grid').isotope({
		  itemSelector: '.grid-item',
		  percentPosition: true,
		  masonry: {
			// use outer width of grid-sizer for columnWidth
			columnWidth: '.grid-item',
		  }
		});


	// filter items on button click
	$('.masonary-menu').on( 'click', 'button', function() {
	  var filterValue = $(this).attr('data-filter');
	  $grid.isotope({ filter: filterValue });
	});

	//for menu active class
	$('.masonary-menu button').on('click', function(event) {
		$(this).siblings('.active').removeClass('active');
		$(this).addClass('active');
		event.preventDefault();
	});

	});

	////////////////////////////////////////////////////
    // 18. Nice Select Js
	$('select').niceSelect();

	////////////////////////////////////////////////////
    // 19. WoW Js
	new WOW().init();

	////////////////////////////////////////////////////
    // 20. Counter Js
	$('.counter').counterUp({
		delay: 100,
		time: 1000
	});
})(jQuery);