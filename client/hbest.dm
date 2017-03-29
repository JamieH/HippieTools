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

client/New()
        . = ..()
                detect_alt(src)

