# -*- coding: utf-8 -*-
import scrapy
import json


class NewhomeSpider(scrapy.Spider):
    name = 'newhome'
    allowed_domains = ['www.newhomesource.com']

    page_num = 1
    payload = """{"searchParameters":{"WebApiSearchType":"Radius","LastFilterApplied":"","FirstFilterApplied":"","Random":0,"FiltersApplied":[],"ComingSoon":false,"GetLocationCoordinates":true,"GetRadius":true,"CustomRadiusSelected":false,"SrpType":"CommunityResults","IsMapVisible":false,"Zoom":5,"IsCurrentLocation":false,"ShowResultsBanner":false,"ResultsBannerPosition":0,"IsBuilderTabSearch":false,"IsMultiLocationSearch":false,"SyntheticInfo":null,"BuilderTypeComm":false,"LocationContext":2,"UseCustomRadius":false,"CurrentSearchHasCustomRadius":false,"UpdateStatusCodeByInactiveBrand":true,"StaticMapZoomLevel":0,"ExcludeLocation":false,"ExcludeBuilders":false,"ExcludeBrands":false,"ExcludeMarkets":false,"ExcludeStates":false,"ContentTypeId":0,"AllowStateSearch":0,"ContentId":0,"BookmarkId":0,"BookmarkUrl":null,"Name":null,"FolderId":null,"UnPublished":0,"Communities":null,"IsJavaScriptEnabled":true,"LastSearchResultsPage":null,"IsMarketSearch":false,"ReviewSortBy":0,"ReviewStar":null,"SegmentId":null,"Reconumber":0,"MarketStateAbbr":"TX","IsCustomFilterActive":false,"IsBoylFilterActive":false,"BasicBrandToTheEnd":false,"ListingId":0,"IsVanityUrl":false,"ShouldExcludeBasicListings":false,"ShouldExcludeBasicCommunities":false,"PartnerId":1,"MarketId":279,"State":"TX","StateName":"Texas","MarketName":"Houston","SearchLocation":null,"ImageCount":0,"OriginLat":29.7806,"OriginLng":-96.156898,"Radius":25,"MinLat":0,"MinLng":0,"MaxLat":0,"MaxLng":0,"Markets":null,"City":"Sealy","Cities":null,"County":"","Counties":null,"PostalCode":"","PostalCodes":null,"BuilderId":0,"Builders":null,"BrandId":0,"Brands":[],"ParentCommId":0,"CommId":0,"CommName":"","Comms":null,"PlanId":0,"PlanName":null,"Plans":null,"SpecId":0,"Specs":null,"LotId":0,"Listings":null,"PageSize":20,"PageNumber":2,"SortBy":"Random","SortFacets":false,"SortOrder":false,"SortFirstBy":"Sealy","SortSecondBy":"Distance","SortSecondOrder":false,"CommIdsSort":null,"PlanIdsSort":null,"SpecIdsSort":null,"SortBySimilarTo":null,"Gated":false,"Pool":false,"GolfCourse":false,"Green":false,"NatureAreas":false,"Parks":false,"Views":false,"Waterfront":false,"Sports":false,"Adult":false,"AgeRestricted":false,"SingleFamily":false,"MultiFamily":false,"Condo":false,"TownHome":false,"Promo":false,"ConsumerPromo":false,"AgentPromo":false,"HotDeals":false,"Event":false,"CommunityStatus":"","HomeStatus":"","AnyHomeStatus":null,"Bedrooms":0,"Bathrooms":0,"Garages":"0.0","LivingAreas":0,"Stories":0,"NumStory":0,"MasterBedLocation":0,"PriceLow":0,"PriceHigh":0,"SqFtLow":0,"SqFtHigh":0,"IncludeImageInfo":false,"ImgCat":null,"ImgColorType":null,"ImgType":null,"MinImgWidth":0,"MinImgHeight":0,"ImgIds":null,"IncludeSphericalImages":false,"SetSphericalAtTheEnd":false,"ThumbnailWidth":0,"ThumbnailHeight":0,"IncludeMpc":true,"LuxuryHomes":false,"Qmi":false,"IncludeBasicMpc":false,"CountsOnly":false,"HotHomes":false,"CustomResults":false,"AlphaResults":true,"NoBoyl":true,"ExcludeRegularComms":false,"Boyl":false,"Custom":false,"Mfr":false,"ExcludeMfr":false,"CustomBuilderLocations":false,"LastCached":false,"Cache":false,"ExtMapPoints":false,"SchoolDistrictIds":"","RandomizeResults":false,"BasicListingToTheEnd":null,"AggregateOptions":false,"BackFillImages":false,"IncludeBookmarks":false,"UserId":null,"IncludeIntMedia":false,"IncludeImages":false,"IncludeVideos":false,"IncludeFplOnSummary":false,"IncludeVideoUrls":false,"HomeCountsFromResults":false,"ApiGeographyPolygonIntersects":null,"ShowBuilderIdsFacet":false,"ShowMarketsFacet":false,"ShortResults":false,"ExcludeBrandsFromResults":false,"HasPlanOptions":false,"HasOpenAmenities":false,"Client":null,"IncludeBrandShowcase":false,"IncludePortfolioHomes":false,"IncludeUrgencyData":false,"CommunityUrl":null,"IncludeHoa":false,"IncludeCommunityUrl":false,"CommunityNumber":null,"IncludeListingUrl":false,"ListingUrl":null,"ListingNumber":null,"ExcludeBasicListings":false},"fromPage":"https://www.newhomesource.com/communities/tx/houston-area/sealy","marketUrl":"https://www.newhomesource.com/communities/tx/houston-area"}"""
    new_payload = json.loads(payload)
    
    def start_requests(self):
        yield scrapy.Request(
            url="https://www.newhomesource.com/ajax/communityresultsv2/getresults/tx/houston-area/sealy",
            method="POST",
            headers={"content-type": "application/json"},
            body=json.dumps(self.new_payload)
        )

    def parse(self, response):
        det = response.xpath("//div[contains(@class, 'result--comm')]")
        for d in det:
            script = d.xpath("(.//script[@type='application/ld+json'])[1]/text()").get()
            s_dict = json.loads(script)
            builder_name = d.xpath(".//p[@data-segment-event-builder_name]/@data-segment-event-builder_name").get()
            community_low_price = d.xpath(".//p[@data-segment-event-community_low_price]/@data-segment-event-community_low_price").get()
            community_high_price = d.xpath(".//p[@data-segment-event-community_high_price]/@data-segment-event-community_high_price").get()

            yield {
                'builder_name': builder_name,
                'community_low_price': community_low_price,
                'community_high_price': community_high_price,
                'name': s_dict.get('name'),
                'telephone': s_dict.get('telephone'),
                'address_locality': s_dict.get('Address').get('addressLocality'),
                'address_region': s_dict.get('Address').get('addressRegion'),
                'postal_code': s_dict.get('Address').get('postalCode'),
                'latitude': s_dict.get('Geo').get('latitude'),
                'longitude': s_dict.get('Geo').get('longitude')

            }

        
        if int(self.new_payload.get('searchParameters').get('PageNumber')) <= 7:
            self.page_num += 1
            self.new_payload['searchParameters']['PageNumber'] = str(self.page_num)

            yield scrapy.Request(
                url="https://www.newhomesource.com/ajax/communityresultsv2/getresults/tx/houston-area/sealy",
                method="POST",
                headers={"content-type": "application/json"},
                body=json.dumps(self.new_payload),
                callback=self.parse
            )


   

        
            

