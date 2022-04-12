        jQuery(function() {
        	function slideMenu() {
        		var activeState = jQuery('#menu-container .menu-list').hasClass('active');
        		jQuery('#menu-container .menu-list').animate({
        			left: activeState ? '0%' : '-100%'
        		}, 400);
        	}
        	jQuery('.alt-menu-btn').click(function(event) {
        		event.stopPropagation();
        		jQuery('.hamburger-menu').toggleClass('open');
        		jQuery('.menu-list').toggleClass('active');
               slideMenu();

               jQuery('body').toggleClass('overflow-hidden');
           });
            
        }); // jQuery load