using System.Collections.Generic;
using System;
using System.ComponentModel;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System.Diagnostics.Tracing;
using System.Drawing;
using System.Runtime.InteropServices;

namespace Neaera_Website_2018

{
    public class configurationObject
    {
        public string DateCreated { get; set; } //only updated when initially created
        // public string DateUpdated { get; set; } //update each time updated
        // public string PublishDate { get; set; } //update each time updated
        public string FeedInfoID { get; set; }
        public GENERALINFO GeneralInfo { get; set; }
        public List<TYPEOFWORK> TypesOfWork { get; set; }
        public LANEINFO LaneInfo { get; set; }
        public SPEEDLIMITS SpeedLimits { get; set; }
        public CAUSE CauseCodes { get; set; }
        public SCHEDULE Schedule { get; set; }
        public LOCATION Location { get; set; }
        public METADATA metadata { get; set; }
        public IMAGEINFO ImageInfo { get; set; }
    }

    public class GENERALINFO
    {
        public string Description { get; set; }
        public string RoadName { get; set; }
        public string RoadNumber { get; set; }
        public DIRECTION? Direction { get; set; }
        public string BeginningCrossStreet { get; set; } //beginning cross street
        public string EndingCrossStreet { get; set; }//ending cross street
        public int BeginningMilePost { get; set; }//int beginning milepost
        public int EndingMilePost { get; set; } //int ending milepost
        public EVENTSTATUS ? EventStatus { get; set; } //calculated
    }

    public class IMAGEINFO
    {
        public int Zoom { get; set; }
        public Coordinate Center { get; set; }
        public List<Marker> Markers { get; set; }
        public string MapType { get; set; }
        public int Height { get; set; }
        public int Width { get; set; }
        public string Format { get; set; }
        public string ImageString { get; set; }
    }
    public class Marker
    {
        public string Name { get; set; }
        public Color Color { get; set; }
        public Coordinate Location { get; set; }
        public Marker(string name, Color color, Coordinate location)
        {
            Name = name;
            Color = color;
            Location = location;
        }
    }

    public class LANEINFO
    {
        public int NumberOfLanes { get; set; }
        public double AverageLaneWidth { get; set; }
        public double ApproachLanePadding { get; set; }
        public double WorkzoneLanePadding { get; set; }
        public int VehiclePathDataLane { get; set; }
        public List<LANE> Lanes { get; set; }
    }
    public class METADATA
    {
        public WZ_LOCATION_METHODS? wz_location_method { get; set; }
        public string lrs_type { get; set; }
        public string location_verify_method { get; set; }
        public int? datafeed_frequency_update { get; set; }
        public string timestamp_metadata_update { get; set; }
        public string contact_name { get; set; }
        public string contact_email { get; set; }
        public string issuing_organization { get; set; } //** textbox


    }
    public class LANE
    {
        public int LaneNumber;
        public LANETYPES LaneType { get; set; }
        public List<LANERESTRICTIONS> LaneRestrictions { get; set; }
    }

    public class LANERESTRICTIONS
    {
        public float? RestrictionValue;
        public RESTRICTIONTYPE RestrictionType { get; set; }
        public RESTRICTIONUNITS? RestrictionUnits { get; set; }
    }

    public class TYPEOFWORK
    {
       public WORKTYPE WorkType { get; set; }
       public bool Is_Architectural_Change; //** check box y/n
    }

    public class SPEEDLIMITS
    {
        public int NormalSpeed { get; set; }
        public int ReferencePointSpeed { get; set; }
        public int WorkersPresentSpeed { get; set; }
    }

    public class CAUSE
    {
        public int CauseCode { get; set; }
        public int SubCauseCode { get; set; }
    }

    public class SCHEDULE
    {
        public string StartDate { get; set; }
        public STARTDATEACCURACY StartDateAccuracy { get; set; }
        public string EndDate { get; set; }
        public ENDDATEACCURACY EndDateAccuracy { get; set; }
        public List<string> DaysOfWeek { get; set; }
    }

    public class LOCATION
    {
        public Coordinate BeginningLocation { get; set; }
        public BEGINNINGACCURACY BeginningAccuracy { get; set; }
        public Coordinate EndingLocation { get; set; }
        public ENDINGACCURACY EndingAccuracy { get; set; }
    }

    public class Coordinate
    {
        public double Lat { get; set; }
        public double Lon { get; set; }
        public double? Elev { get; set; }
        public Coordinate()
        {

        }
        public Coordinate(double lat, double lon)
        {
            Lat = lat;
            Lon = lon;
        }
        public Coordinate(double lat, double lon, double? elev)
        {
            Lat = lat;
            Lon = lon;
            Elev = elev;
        }
    }

    [JsonConverter(typeof(CustomStringEnumConverter))]
    public enum EVENTSTATUS
    {
        [Description("planned")] planned,
        [Description("pending")] pending,
        [Description("active")] active,
        [Description("cancelled")] cancelled,
        [Description("completed")] completed
    }
    [JsonConverter(typeof(CustomStringEnumConverter))]
    public enum BEGINNINGACCURACY
    {
        [Description("estimated")] estimated,
        [Description("verified")] verified
    }
    [JsonConverter(typeof(CustomStringEnumConverter))]
    public enum ENDINGACCURACY
    {
        [Description("estimated")] estimated,
        [Description("verified")] verified
    }
    [JsonConverter(typeof(CustomStringEnumConverter))]
    public enum STARTDATEACCURACY
    {
        [Description("estimated")] estimated,
        [Description("verified")] verified
    }
    [JsonConverter(typeof(CustomStringEnumConverter))]
    public enum ENDDATEACCURACY
    {
        [Description("estimated")] estimated,
        [Description("verified")] verified
    }
    [JsonConverter(typeof(CustomStringEnumConverter))]
    public enum DIRECTION
    {
        [Description("northbound")] northbound,
        [Description("eastbound")] eastbound ,
        [Description("southbound")] southbound,
        [Description("westbound")] westbound
    }
    [JsonConverter(typeof(CustomStringEnumConverter))]
    public enum WORKTYPE
    {
        [Description("maintenance")] maintenance,
        [Description("minor-road-defect-repair")] minorroaddefectrepair,
        [Description("roadside-work")] roadsidework,
        [Description("overhead-work")] overheadwork,
        [Description("below-road-work")] belowroadwork,
        [Description("barrier-work")] barrierwork,
        [Description("surface-work")] surfacework,
        [Description("painting")] painting,
        [Description("roadway-relocation")] roadwayrelocation,
        [Description("roadway-creation")] roadwaycreation
    }
    [JsonConverter(typeof(CustomStringEnumConverter))]
    public enum RESTRICTIONTYPE
    {
        [Description("no-trucks")] notrucks,
        [Description("travel-peak-hours-only")] travelpeakhoursonly,
        [Description("hov-3")] hov3,
        [Description("hov-2")] hov2,
        [Description("no-parking")] noparking,
        [Description("reduced-width")] reducedwidth,
        [Description("reduced-height")] reducedheight,
        [Description("reduced-length")] reducedlength,
        [Description("reduced-weight")] reducedweight,
        [Description("axle-load-limit")] axleloadlimit,
        [Description("gross-weight-limit")]  grossweightlimit,
        [Description("towing-prohibited")] towingprohibited,
        [Description("permitted-oversize-loads-prohibited")] permittedoversizeloadsprohibitied
    }
    [JsonConverter(typeof(CustomStringEnumConverter))]
    public enum LANETYPES
    {
        [Description("left-lane")] leftlane,
        [Description("right-lane")] rightlane,
        [Description("center-lane")] centerlane,
        [Description("middle-lane")] middlelane,
        [Description("right-turning-lane")] rightturninglane,
        [Description("left-turning-lane")] leftturninglane,
        [Description("right-exit-lane")] rightexitlane,
        [Description("left-exit-lane")] leftexitlane,
        [Description("right-mergining-lane")] rightmergininglane,
        [Description("left-merging-lane")] leftmerginglane,
        [Description("right-exit-ramp")] rightexitramp,
        [Description("sidewalk")] sidewalk,
        [Description("bike-lane")] bikelane,
        [Description("right-shoulder")] rightshoulder,
        [Description("left-shoulder")] leftshoulder
        /* REMOVED 3/16/21 Because RSM failed to load
         * [Description("all-roadways")] allroadways
        [Description("through-lanes")] throughlanes,
        [Description("middle-two-lanes")] middletwolanes,*/
    }
    [JsonConverter(typeof(CustomStringEnumConverter))]
    public enum RESTRICTIONUNITS 
    {
        [Description("feet")] feet,
        [Description("inches")] inches,
        [Description("centimeters")] centimeters,
        [Description("pounds")] pounds,
        [Description("tons")] tons,
        [Description("kilograms")] kilograms 
    }
    [JsonConverter(typeof(CustomStringEnumConverter))]
    public enum WZ_LOCATION_METHODS
    {
        [Description("channel-device-method")] channeldevicemethod,
        [Description("sign-method")] signmethod,
        [Description("junction-method")] junctionmethod,
        [Description("unknown ")] unknown,
        [Description("other ")] other
    }
    public class CustomStringEnumConverter : Newtonsoft.Json.Converters.StringEnumConverter
    {
        public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer)
        {
            Type type = value.GetType() as Type;
            if (value == null)
            {
                string val = null;
                writer.WriteValue(val);
            }
            if (!type.IsEnum)
            {
                Type u = Nullable.GetUnderlyingType(type);
                if (u == null || !u.IsEnum) throw new InvalidOperationException("Only type Enum is supported");
                else type = u;
            }
            foreach (var field in type.GetFields())
            {
                if (field.Name == value.ToString())
                {
                    var attribute = Attribute.GetCustomAttribute(field, typeof(DescriptionAttribute)) as DescriptionAttribute;
                    writer.WriteValue(attribute != null ? attribute.Description : field.Name);

                    return;
                }
            }

            throw new ArgumentException("Enum not found");
        }
        public override object ReadJson(JsonReader reader, Type type, object value, JsonSerializer serializer)
        {
            value = reader.Value;
            if (value == null) return null;
            if (!type.IsEnum)
            {
                Type u = Nullable.GetUnderlyingType(type);
                if (u == null || !u.IsEnum) throw new InvalidOperationException("Only type Enum is supported");
                else type = u;
            }
            foreach (var field in type.GetFields())
            {
                var attribute = Attribute.GetCustomAttribute(field, typeof(DescriptionAttribute)) as DescriptionAttribute;
                if (attribute != null && attribute.Description.ToString() == value.ToString())
                {
                    return Enum.Parse(type, field.Name.ToString());
                }
                else if (field.Name == value.ToString())
                {
                    return Enum.Parse(type, field.Name.ToString());
                }
            }

            throw new ArgumentException("Enum not found");
        }
    }
}