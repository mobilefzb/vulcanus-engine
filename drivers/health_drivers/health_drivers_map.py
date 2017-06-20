import health_drivers.httpdriver as httpdriver
import health_drivers.rabbitmqdriver as rabbitmqdriver
import health_drivers.shellscriptdriver as shellscriptdriver

DRIVER_MAP = {
	"HTTPClient" : httpdriver.check_health_with_policy,
	"RabbitMQClient" : rabbitmqdriver.check_health_with_policy,
	"ShellScriptClient" : shellscriptdriver.check_health_with_policy
}