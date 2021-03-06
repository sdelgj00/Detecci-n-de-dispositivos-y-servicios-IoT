"Serialize & parse WS-Discovery Bye SOAP messages"

from ..namespaces import NS_ADDRESSING, NS_DISCOVERY, NS_ACTION_BYE
from ..envelope import SoapEnvelope
from ..util import createSkelSoapMessage, getBodyEl, getHeaderEl, addElementWithText, \
                   addTypes, addScopes, getDocAsString, getScopes, addEPR, \
                   _parseAppSequence


def createByeMessage(env):
    "serialize a SOAP envelope object into a string"
    doc = createSkelSoapMessage(NS_ACTION_BYE)

    bodyEl = getBodyEl(doc)
    headerEl = getHeaderEl(doc)

    addElementWithText(doc, headerEl, "a:MessageID", NS_ADDRESSING, env.getMessageId())
    addElementWithText(doc, headerEl, "a:To", NS_ADDRESSING, env.getTo())

    appSeqEl = doc.createElementNS(NS_DISCOVERY, "d:AppSequence")
    appSeqEl.setAttribute("InstanceId", env.getInstanceId())
    appSeqEl.setAttribute("MessageNumber", env.getMessageNumber())
    headerEl.appendChild(appSeqEl)

    byeEl = doc.createElementNS(NS_DISCOVERY, "d:Bye")
    addEPR(doc, byeEl, env.getEPR())
    bodyEl.appendChild(byeEl)

    return getDocAsString(doc)


def parseByeMessage(dom):
    "parse a XML message into a SOAP envelope object"
    env = SoapEnvelope()
    env.setAction(NS_ACTION_BYE)

    env.setMessageId(dom.getElementsByTagNameNS(NS_ADDRESSING, "MessageID")[0].firstChild.data.strip())
    env.setTo(dom.getElementsByTagNameNS(NS_ADDRESSING, "To")[0].firstChild.data.strip())

    _parseAppSequence(dom, env)

    env.setEPR(dom.getElementsByTagNameNS(NS_ADDRESSING, "Address")[0].firstChild.data.strip())

    return env



