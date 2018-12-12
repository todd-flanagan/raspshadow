from subprocess import Popen, PIPE
import json

def findOrCreateNewThing(newThing):
    p = Popen(["aws", "iot", "list-things"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    #print(output)
    #print(json.loads(output))
    thingsDict = json.loads(output)
    print(thingsDict["things"][0]["thingArn"])

    things = {}
    for thing in thingsDict["things"]:
      things[thing["thingName"]] =  thing["thingArn"]


    thingArn = ""

    if not newThing in things:

        # create a new thing
        p = Popen(["aws", "iot", "create-thing", "--thing-name", newThing], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        print(output)
        print(json.loads(output))
        thingsDict = json.loads(output)
        print(thingsDict["thingName"])
        print(thingsDict["thingArn"])
        arn = thingsDict["thingArn"]
        print(thingsDict["thingId"])
    else:
        thingArn = things[newThing]

    return thingArn

def createAndAttachCertificate(newThing, thingArn):
    #setup and attach the certificate for the thing to communicate through
    #if the thing has no principals, create a certificate and an iot policy.  Attach the
    #policy to the certificate and then the certificate to the thing

    p = Popen(["aws", "iot", "list-thing-principals", "--thing-name", newThing], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    #print(output)
    #print(json.loads(output))
    principalsDict = json.loads(output)
    if not principalsDict["principals"]:
      print("no cert")
      p = Popen(["aws", "iot", "create-keys-and-certificate", \
                               "--set-as-active", \
                               "--certificate-pem-outfile", "./certificates/" + newThing + ".pem", \
                               "--public-key-outfile" , "./certificates/" + newThing + "public.pem", \
                               "--private-key-outfile" , "./certificates/" + newThing + "private.pem"], \
                               stdin=PIPE, stdout=PIPE, stderr=PIPE)
      output, err = p.communicate()
      print(output)
      print(json.loads(output))
      certificatDict = json.loads(output)
      certificateArn = certificatDict["certificateArn"]


      #create the policy
      p = Popen(["aws", "iot", "create-policy", \
                               "--policy-name", newThing + "Policy" \
                               "--policy-document", "file:///Users/tflanaga/work/iot/raspshadow/thingPolicy.json"],
                               stdin=PIPE, stdout=PIPE, stderr=PIPE)
      output, err = p.communicate()

      print(output)
      policyDict = json.loads(output)
      policyArn = policyDict["policyArn"]


      #attach the policy to the certificate
      p = Popen(["aws", "iot", "attach-policy", \
                               "--policy-name", newThing + "Policy" \
                               "--target", certificateArn],
                               stdin=PIPE, stdout=PIPE, stderr=PIPE)
      output, err = p.communicate()

      print(output)
      policyDict = json.loads(output)
      policyArn = policyDict["policyArn"]

      #attach the certificate to the thing
      p = Popen(["aws", "iot", "attach-thing-principal", \
                               "--thing-name", newThing, \
                               "--principal", certificateArn],
                               stdin=PIPE, stdout=PIPE, stderr=PIPE)
      output, err = p.communicate()



    else:
      print(principalsDict["principals"])

    return certificateArn




newThing = "macDesktopThing"
arn = findOrCreateNewThing(newThing)
print(arn)
certArn = createAndAttachCertificate(newThing, arn)
print(certArn)
