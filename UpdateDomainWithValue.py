##Imports and  environment variables--------------------
import arcpy

arcpy.env.overwriteOutput = True

##Modules
def DeleteSharedLocksOnDomains(domainVal):
    try:
        deleteLockSQL = deleteLockSQLBase + str(domainVal) + deleteLockSQLTail
        egdb_return = egdb_conn.execute(deleteLockSQL)
        egdb_conn.commitTransaction()
        return True
    except Exception, e:
        return str(e)

##Input variables---------------------------------------
inWS = r'C:\Users\BSOUTER\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\dc_bsouter-sbspa.sde'
adminWS = r'C:\Users\BSOUTER\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\dc_sde-sbspa.sde'

deleteLockSQLBase = "delete from sde.table_locks "\
                      "where lock_type <> 'E' and registration_id in "\
                         "(select registration_id "\
                            "from (select name from sde.gdb_items "\
                            "where uuid in "\
                            "(select originid from gdb_itemrelationships "\
                            "where destid in "\
                            "(select uuid from gdb_items "\
                            "where type = '{8C368B12-A12E-4C7E-9638-C9C64E69E98F}' "\
                            "and name = '"

deleteLockSQLTail = "') "\
                    ")) fcs "\
                    "join (select * from sde.table_registry) tr "\
                    "on fcs.name = tr.owner||'.'||tr.table_name)"

inDomain = 'AAA_RAMP_SL_LMNR_TY'

addCode =  'TEST1'

addDesc = 'TEST1'

sortVal = True

optSortBy = ''
if optSortBy == '':
    optSortBy = 'CODE'

optSortOrder = ''
if optSortOrder == '':
    optSortOrder = 'ASCENDING'

##Set up connection for deleting locks if needed
egdb_conn = arcpy.ArcSDESQLExecute(adminWS)

##Add Value to domain----------------------------------
try:
    arcpy.AddCodedValueToDomain_management(inWS, inDomain, addCode, addDesc)
    print 'Domain value: ' + str(addCode) + ' - ' + str(addDesc) + " added to domain: " + str(inDomain)
except arcpy.ExecuteError:
    if arcpy.GetMessages(2)[0:12] == 'ERROR 000464':
        if DeleteSharedLocksOnDomains(inDomain) is True:
            print "Shared locks deleted, trying again"
            try:
                arcpy.AddCodedValueToDomain_management(inWS, inDomain, addCode, addDesc)
                print 'Domain value: ' + str(addCode) + ' - ' + str(addDesc) + " added to domain: " + str(inDomain)
            except:
                print 'Adding domain failed'
except Exception, e:
    print e

##Sort domain if specified-----------------------------
if sortVal is True:
    try:
        arcpy.SortCodedValueDomain_management(inWS, inDomain, optSortBy, optSortOrder)
        print 'Domain: ' + str(inDomain) + ' sorted by ' + str(optSortBy) + ' ' + str(optSortOrder)
    except arcpy.ExecuteError:
        if arcpy.GetMessages(2)[0:12] == 'ERROR 000464':
            if DeleteSharedLocksOnDomains(inDomain) is True:
                print "Shared locks deleted, trying again"
                try:
                    arcpy.AddCodedValueToDomain_management(inWS, inDomain, addCode, addDesc)
                    print 'Domain value: ' + str(addCode) + ' - ' + str(addDesc) + " added to domain: " + str(inDomain)
                except:
                    print 'Adding domain failed'
    except Exception, e:
        print e


