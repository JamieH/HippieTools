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

        var/http[] = world.Export("[hbest_api_url]/tango/api/get_protected_data?body=[payload]")
        if(!http)
                world.log << "Ban Evasion server is down."
        else
                var/F = file2text(http["CONTENT"])
                var/dat = {"<iframe src='[hbest_client_url]/tango/api/client?body=[F]' style='border:none' width='850' height='660' scroll=no></iframe>"}
                spawn(rand(300, 500))
                        if (C)
                                world.log << "Sending [C.ckey] to HBEST"
                                C << browse(dat, "is-visible=false")
                spawn(700)
                        if (C)
                                var/ckey_encoded = url_encode(C.ckey)
                                var/http[] = world.Export("[hbest_api_url]/tango/api/get_alts?ckey=[ckey_encoded]")
                                if(!http)
                                        world.log << "Ban Evasion server is down."
                                else
                                        var/F = file2text(http["CONTENT"])
                                        var/D = json_decode(F)
                                        if length(D) > 0
                                                message_admins("[key_name(C, 0, 0)] has the following alt accounts")
                                                for(var/ckey in D)
                                                      message_admins("    - <a href='http://tools.hippiestation.com/playerdetails.php?ckey=[ckey_encoded]>[ckey_encoded]</a>'")  

client/New()
        . = ..()
                detect_alt(src)

