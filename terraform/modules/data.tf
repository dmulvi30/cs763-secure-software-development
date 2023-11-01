##################
## Account Data ##
##################

data "aws_region" "current" {}

##############
## Route-53 ##
##############

data "aws_route53_zone" "bum_tv" {
  name         = "bumtelevision.com"
  private_zone = false
}
