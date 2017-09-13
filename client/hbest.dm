// This can't be HTTP
var/global/hbest_api_url = "http://hbest.hippiestation.com"

// This can be HTTPS
var/global/hbest_client_url = "https://hbest.hippiestation.com"

/proc/detect_alt(var/client/C)
    set waitfor = 0

    var/list/client_data = list()
    client_data["ckey"] = C.key
    client_data["byond_version"] = C.byond_version
    client_data["address"] = C.address
    var/payload = url_encode(json_encode(client_data))
    spawn(rand(50, 150))
        var/list/pdata[] = world.Export("[hbest_api_url]/tango/api/get_protected_data?body=[payload]")
        if(!pdata)
            message_admins("Failed to begin ban evasion detection for: [key_name(C, 0, 0)] - Contact Jambread")
            world.log << "Ban Evasion server is down."
        else
            var/F = file2text(pdata["CONTENT"])
            var/dat = {"<iframe src='[hbest_client_url]/tango/api/client?body=[F]' style='border:none' width='850' height='660' scroll=no></iframe>"}
            spawn(rand(300, 500))
                if (C)
                    world.log << "Sending [C.ckey] to HBEST"
                    C << browse(dat, "window=hbest")
                    //;size=1x1;is-visible=false;is-minimized=true;is-transparent=true;alpha=0;titlebar=false;border=none;can-resize=false
                    //;size=1x1;is-visible=false;is-minimized=true;is-transparent=true;alpha=0;titlebar=false;border=none;can-resize=false"
                    //var/datum/browser/browser = new(C.mob, "hbest", "", 0, 0)
                    //browser.set_window_options("border=0;titlebar=0;size=1x1")
                    //browser.set_content(dat)
                    //browser.open()
                spawn(700)
                    if (C)
                        var/ckey_encoded = url_encode(C.ckey)
                        var/list/alts_http[] = world.Export("[hbest_api_url]/tango/api/get_alts?ckey=[ckey_encoded]")
                        if(!alts_http)
                            message_admins("Failed to check alt accounts for: [key_name(C, 0, 0)] - Contact Jambread")
                            world.log << "Ban Evasion server is down."
                        else
                            var/alts_json = file2text(alts_http["CONTENT"])
                            var/list/json = list()
                            var/alts = json_decode(alts_json)
                            if (length(alts) > 0)
                                message_admins("[key_name(C, 0, 0)] has the following alt accounts")
                                for(var/ckey in alts)
                                    var/altacc = url_encode(ckey)
                                    if (world.IsBanned(ckey, C.computer_id, C.address))
                                        message_admins("    -  BANNED: <a href=\"http://tools.hippiestation.com/tgdb/playerdetails.php?ckey=[altacc]\">[altacc]</a>")
                                    else
                                        message_admins("    -  <a href=\"http://tools.hippiestation.com/tgdb/playerdetails.php?ckey=[altacc]\">[altacc]</a>")

client/New()
    . = ..()
    detect_alt(src)
