<xsl:stylesheet version="1.0" xmlns:europarl-turn="www.eml.org/NameSpaces/europarl-turn" xmlns:mmax="org.eml.MMAX2.discourse.MMAX2DiscourseLoader" xmlns:sentence="www.eml.org/NameSpaces/sentence" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output indent="no" method="text" omit-xml-declaration="yes" />
<xsl:strip-space elements="*" />
<xsl:template match="words">
<xsl:apply-templates />
</xsl:template>
<xsl:template match="word">
<xsl:value-of select="mmax:registerDiscourseElement(@id)" />
<xsl:apply-templates mode="opening" select="mmax:getStartedMarkables(@id)" />
<xsl:value-of select="mmax:setDiscourseElementStart()" />
<xsl:apply-templates />
<xsl:value-of select="mmax:setDiscourseElementEnd()" />
<xsl:apply-templates mode="closing" select="mmax:getEndedMarkables(@id)" />
<xsl:text> </xsl:text>
</xsl:template>
<xsl:template match="europarl-turn:markable" mode="opening">
<xsl:value-of select="mmax:startBold()" />
<xsl:text>[</xsl:text>
<xsl:value-of select="@europarl-turn" />
<xsl:text>] </xsl:text>
<xsl:value-of select="mmax:endBold()" />
</xsl:template>
<xsl:template match="europarl-turn:markable" mode="closing">
<xsl:text>

</xsl:text>
</xsl:template>
<xsl:template match="sentence:markable" mode="closing">
<xsl:text>
</xsl:text>
</xsl:template>
</xsl:stylesheet>
