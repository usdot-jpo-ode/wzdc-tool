using System.Collections.Generic;
using System;
using System.ComponentModel;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System.Diagnostics.Tracing;

namespace Neaera_Website_2018

{
    public class configObj_json
    {
        public string DateCreated { get; set; } //only updated when initially created
       // public string DateUpdated { get; set; } //update each time updated
       // public string PublishDate { get; set; } //update each time updated

        //public SERIALPORT SERIALPORT { get; set; }
        //public FILES FILES { get; set; }
        //public LANES LANES { get; set; }
        //public SPEED SPEED { get; set; }
        //public CAUSE CAUSE { get; set; }
        //public SCHEDULE SCHEDULE { get; set; }
        //public LOCATION LOCATION { get; set; }
        //public INFO INFO { get; set; }
    }
    //public class INFO
    //{
    //    public string RoadName { get; set; }
    //    public string RoadNumber { get; set; }

    //    public string SubIdentifier { get; set; }
    //    public string IssuingOrganization { get; set; } //** textbox
    //    public string BeginningCrossStreet { get; set; } //beginning cross street
    //    public string EndingCrossStreet { get; set; }//ending cross street
    //    public float BeginningMilePost { get; set; }//int beginning milepost
    //    public float EndingMilePost { get; set; } //int ending milepost
    //    public EVENTSTATUS ? EventStatus { get; set; } //calculated
    //    public BEGINNINGACCURACY ? BeginningAccuracy { get; set; }
    //    public ENDINGACCURACY ? EndingAccuracy { get; set; }
    //    public ENDDATEACCURACY ? EndDateAccuracy { get; set; }
    //    public STARTDATEACCURACY ? StartDateAccuracy { get; set; }
    //    public DIRECTION ? Direction { get; set; }

    //    public List<LANERESTRICTIONS> LaneRestrictions { get; set; } //add grid defaulted to number of lanes
    //    public List<LANETYPE> LaneType { get; set; } //add grid defaulted to number of lanes
    //    public List<TYPEOFWORK> TypeOfWork { get; set; } //add grid add to it with options

    //}
    //public class LANETYPE
    //{
    //    //Lane Edge Reference - put label on screen and make it defaulted to LEFT - TAKE THIS OUT LATER
    //    public int LaneNumber;
    //    public LANETYPES LaneTypes { get; set; }
    //    //see help here https://stackoverflow.com/questions/2373986/how-can-i-use-a-special-char-in-a-c-sharp-enum

    //}
    //public class LANERESTRICTIONS
    //{
    //    public float? RestrictionValue;
    //    public RESTRICTIONTYPE RestrictionType { get; set; }
    //    public RESTRICTIONUNITS? RestrictionUnits { get; set; }
    //    public int LaneNumber;
    //}
    //public class TYPEOFWORK
    //{
    //   public WORKTYPE WorkType { get; set; }
    //   public bool Is_Architectural_Change; //** check box y/n
    //}
    //public class SERIALPORT
    //{
    //    public int SerialBaudrate { get; set; }
    //    public int DataRate { get; set; }
    //    public string SerialPort { get; set; }
    //    public int SerialTimeout { get; set; }
    //}
    //public class FILES
    //{
    //    public string CfgInputFile { get; set; }
    //    public string CfgOutputFile { get; set; }
    //    public string VehiclePathDataDir { get; set; }
    //    public string VehiclePathDataFile { get; set; }
    //}

    //public class LANES
    //{
    //    public string Description { get; set; }
    //    public int NumberOfLanes { get; set; }
    //    public double AverageLaneWidth { get; set; }
    //    public double ApproachLanePadding { get; set; }
    //    public double WorkzoneLanePadding { get; set; }
    //    public int VehiclePathDataLane { get; set; }
    //}

    //public class SPEED
    //{
    //    public int NormalSpeed { get; set; }
    //    public int ReferencePointSpeed { get; set; }
    //    public int WorkersPresentSpeed { get; set; }
    //}

    //public class CAUSE
    //{
    //    public int CauseCode { get; set; }
    //    public int SubCauseCode { get; set; }
    //}

    //public class SCHEDULE
    //{
    //    public string  WZStartDate { get; set; }
    //    public string WZStartTime { get; set; }
    //    public string WZEndDate { get; set; }
    //    public string WZEndTime { get; set; }
    //    public List<string> WZDaysOfWeek { get; set; }
    //}

    //public class LOCATION
    //{
    //    public double WZStartLat { get; set; }
    //    public double WZStartLon { get; set; }
    //    public double WZEndLat { get; set; }
    //    public double WZEndLon { get; set; }
    //}
    //[JsonConverter(typeof(CustomStringEnumConverter))]
    //public enum EVENTSTATUS
    //{
    //    [Description("planned")] planned,
    //    [Description("pending")] pending,
    //    [Description("active")] active,
    //    [Description("cancelled")] cancelled,
    //    [Description("completed")] completed
    //}
    //[JsonConverter(typeof(CustomStringEnumConverter))]
    //public enum BEGINNINGACCURACY
    //{
    //    [Description("estimated")] estimated,
    //    [Description("verified")] verified
    //}
    //[JsonConverter(typeof(CustomStringEnumConverter))]
    //public enum ENDINGACCURACY
    //{
    //    [Description("estimated")] estimated,
    //    [Description("verified")] verified
    //}
    //[JsonConverter(typeof(CustomStringEnumConverter))]
    //public enum STARTDATEACCURACY
    //{
    //    [Description("estimated")] estimated,
    //    [Description("verified")] verified
    //}
    //[JsonConverter(typeof(CustomStringEnumConverter))]
    //public enum ENDDATEACCURACY
    //{
    //    [Description("estimated")] estimated,
    //    [Description("verified")] verified
    //}
    //[JsonConverter(typeof(CustomStringEnumConverter))]
    //public enum DIRECTION
    //{
    //    [Description("northbound")] northbound,
    //    [Description("eastbound")] eastbound ,
    //    [Description("southbound")] southbound,
    //    [Description("westbound")] westbound
    //}
    //[JsonConverter(typeof(CustomStringEnumConverter))]
    //public enum WORKTYPE
    //{
    //    [Description("maintenance")] maintenance,
    //    [Description("minor-road-defect-repair")] minorroaddefectrepair,
    //    [Description("roadside-work")] roadsidework,
    //    [Description("overhead-work")] overheadwork,
    //    [Description("below-road-work")] belowroadwork,
    //    [Description("barrier-work")] barrierwork,
    //    [Description("surface-work")] surfacework,
    //    [Description("painting")] painting,
    //    [Description("roadway-relocation")] roadwayrelocation,
    //    [Description("roadway-creation")] roadwaycreation
    //}
    //[JsonConverter(typeof(CustomStringEnumConverter))]
    //public enum RESTRICTIONTYPE
    //{
    //    [Description("no-trucks")] notrucks,
    //    [Description("travel-peak-hours-only")] travelpeakhoursonly,
    //    [Description("hov-3")] hov3,
    //    [Description("hov-2")] hov2,
    //    [Description("no-parking")] noparking,
    //    [Description("reduced-width")] reducedwidth,
    //    [Description("reduced-height")] reducedheight,
    //    [Description("reduced-length")] reducedlength,
    //    [Description("reduced-weight")] reducedweight,
    //    [Description("axle-load-limit")] axleloadlimit,
    //    [Description("gross-weight-limit")]  grossweightlimit,
    //    [Description("towing-prohibited")] towingprohibited,
    //    [Description("permitted-oversize-loads-prohibited")] permittedoversizeloadsprohibitied
    //}
    //[JsonConverter(typeof(CustomStringEnumConverter))]
    //public enum LANETYPES
    //{
    //    [Description("all-roadways")] allroadways,
    //    [Description("through-lanes")] throughlanes,
    //    [Description("left-lane")] leftlane,
    //    [Description("right-lane")] rightlane,
    //    [Description("center-lane")] centerlane,
    //    [Description("middle-lane")] middlelane,
    //    [Description("middle-two-lanes")] middletwolanes,
    //    [Description("right-turning-lanes")] rightturninglanes,
    //    [Description("left-turing-lanes")] leftturinglanes,
    //    [Description("right-exit-lanes")] rightexitlanes,
    //    [Description("left-exit-lanes")] leftexitlanes,
    //    [Description("right-mergining-lanes")] rightmergininglanes,
    //    [Description("left-merging-lanes")] leftmerginglanes,
    //    [Description("right-exit-ramp")] rightexitramp,
    //    [Description("sidewalk")] sidewalk,
    //    [Description("bike-lane")] bikelane,
    //    [Description("right-shoulder-outside")] rightshoulderoutside,
    //    [Description("left-shoulder")] leftshoulder
    //}
    //// [JsonConverter(typeof(CustomStringEnumConverter))]
    //public enum RESTRICTIONUNITS 
    //{
    //    [Description("ft")] feet,
    //    [Description("in")] inches,
    //    [Description("cm")] centimeters,
    //    [Description("lbs")] pounds,
    //    [Description("tons")] tons,
    //    [Description("kg")] kilograms 
    //}

    //public class CustomStringEnumConverter : Newtonsoft.Json.Converters.StringEnumConverter
    //{
    //    public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer)
    //    {
    //        Type type = value.GetType() as Type;
    //        if (value == null)
    //        {
    //            string val = null;
    //            writer.WriteValue(val);
    //        }
    //        if (!type.IsEnum)
    //        {
    //            Type u = Nullable.GetUnderlyingType(type);
    //            if (u == null || !u.IsEnum) throw new InvalidOperationException("Only type Enum is supported");
    //            else type = u;
    //        }
    //        foreach (var field in type.GetFields())
    //        {
    //            if (field.Name == value.ToString())
    //            {
    //                var attribute = Attribute.GetCustomAttribute(field, typeof(DescriptionAttribute)) as DescriptionAttribute;
    //                writer.WriteValue(attribute != null ? attribute.Description : field.Name);

    //                return;
    //            }
    //        }

    //        throw new ArgumentException("Enum not found");
    //    }
    //    public override object ReadJson(JsonReader reader, Type type, object value, JsonSerializer serializer)
    //    {
    //        value = reader.Value;
    //        if (value == null) return null;
    //        if (!type.IsEnum)
    //        {
    //            Type u = Nullable.GetUnderlyingType(type);
    //            if (u == null || !u.IsEnum) throw new InvalidOperationException("Only type Enum is supported");
    //            else type = u;
    //        }
    //        foreach (var field in type.GetFields())
    //        {
    //            var attribute = Attribute.GetCustomAttribute(field, typeof(DescriptionAttribute)) as DescriptionAttribute;
    //            if (attribute != null && attribute.Description.ToString() == value.ToString())
    //            {
    //                return Enum.Parse(type, field.Name.ToString());
    //            }
    //            else if (field.Name == value.ToString())
    //            {
    //                return Enum.Parse(type, field.Name.ToString());
    //            }
    //        }

    //        throw new ArgumentException("Enum not found");
    //    }
    //}
}