/*
 * JavaScript file for the application to demonstrate
 * using the API
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() 
{
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/dailyDonor',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
		/*,
        create: function(dailyDonor) {
            let ajax_options = {
                type: 'POST',
                url: 'api/dailyDonor',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(dailyDonor)
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        update: function(dailyDonor) {
            let ajax_options = {
                type: 'PUT',
                url: `api/dailyDonors/${dailyDonor.dailyDonor_id}`,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(dailyDonor)
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_update_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        'delete': function(dailyDonor_id) {
            let ajax_options = {
                type: 'DELETE',
                url: `api/dailyDonors/${dailyDonor_id}`,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
		*/
    };
}());

// Create the view instance
ns.view = (function() 
{
    'use strict';

    let $regionid = $('#regionID'),
        $locationName = $('#locationName'),
        $donationType = $('#donationType'),
		$yearmonthdayNum = $('#yearmonthdayNum'),
        $yearmonthdayName = $('#yearmonthdayName'),
		$numDonors = $('#numDonors');

    // return the API
    return {
        reset: function() {
            $regionid.val('');
            $locationName.val('');
            $donationType.val('').focus(),
			$yearmonthdayNum.val(''),
			$yearmonthdayName.val(''),
			$numDonors.val('');
        },
        update_editor: function(dailyDonor) {
            $regionid.val(dailyDonor.regionid);
            $locationName.val(dailyDonor.locationName);
            $donationType.val(dailyDonor.donationType).focus();
			$yearmonthdayNum.val(dailyDonor.yearmonthdayNum);
			$yearmonthdayName.val(dailyDonor.yearmonthdayName);
			$numDonors.val(dailyDonor.numDonors);
        },
        build_table: function(dailyDonors) {
            let rows = ''

            // clear the table
            $('.dailyDonors table > tbody').empty();

            // did we get a dailyDonors array?
            if (dailyDonors) {
                for (let i=0, l=dailyDonors.length; i < l; i++) {
                    rows += `<tr data-dailyDonor-id="${dailyDonors[i].dailyDonor_id}">
                        <td class="donationType">${dailyDonors[i].donationType}</td>
                        <td class="locationName">${dailyDonors[i].locationName}</td>
						<td class="yearmonthdayNum">${dailyDonors[i].yearmonthdayNum}</td>
						<td class="yearmonthdayName">${dailyDonors[i].yearmonthdayName}</td>
                        <td class="numDonors">${dailyDonors[i].numDonors}</td>
						<td>${dailyDonors[i].timestamp}</td>
                    </tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $dailyDonor_id = $('#dailyDonor_id'),
        $donationType = $('#donationType'),
        $locationName = $('#locationName'),
		$yearmonthdayNum = $('#yearmonthdayNum'),
		$yearmonthdayName = $('#yearmonthdayName'),
		$numDonors = $('#numDonors')		
		;

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100)

    // Validate input
    function validate(donationType, locationName) {
        return donationType !== "" && locationName !== "";
    }

    // Create our event handlers
    $('#create').click(function(e) {
        let donationType = $donationType.val(),
            locationName = $locationName.val();

        e.preventDefault();

        if (validate(donationType, locationName)) {
            model.create({
                'donationType': donationType,
                'locationName': locationName,
            })
        } else {
            alert('Problem with first or last name input');
        }
    });

    $('#update').click(function(e) {
        let dailyDonor_id = $dailyDonor_id.val(),
            donationType = $donationType.val(),
            locationName = $locationName.val();

        e.preventDefault();

        if (validate(donationType, locationName)) {
            model.update({
                dailyDonor_id: dailyDonor_id,
                donationType: donationType,
                locationName: locationName,
            })
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#delete').click(function(e) {
        let dailyDonor_id = $dailyDonor_id.val();

        e.preventDefault();

        if (validate('placeholder', locationName)) {
            model.delete(dailyDonor_id)
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#reset').click(function() {
        view.reset();
    })

    $('table > tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target),
            dailyDonor_id,
            donationType,
            locationName;

        dailyDonor_id = $target
            .parent()
            .attr('data-dailyDonor-id');

        donationType = $target
            .parent()
            .find('td.donationType')
            .text();

        locationName = $target
            .parent()
            .find('td.locationName')
            .text();

        view.update_editor({
            dailyDonor_id: dailyDonor_id,
            donationType: donationType,
            locationName: locationName,
        });
    });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));
